"""SSE 解析原语，不依赖任何 HTTP 客户端。

这里只实现 OpenAI 使用的 data-only SSE 子集：空行分派事件，多个 ``data:``
行按 LF 拼接；``event`` / ``id`` / ``retry`` 字段不参与请求恢复，直接忽略。
"""

from ..errors	import SSEParseError
from ..models	import StreamChunk

import codecs
import logging

from typing import Any, Iterator, List, Optional

logger = logging.getLogger(__name__)

# 单次读取的字节数，与 aiohttp 的 iter_chunked 配合使用。
READ_CHUNK_SIZE = 1024

# 这是单条流内的容错预算，不是 HTTP 重试次数；成功解析一个 chunk 会重置连续失败计数。
MAX_SSE_PARSE_ERRORS = 3

# [DONE] 是 OpenAI 风格的控制载荷，不是可验证的 StreamChunk；用哨兵
# 与 None（被容忍跳过的事件）和正常 chunk 区分开来。
DONE = object()

_DONE_PAYLOAD = "[DONE]"

class SSEDecoder:

	"""把字节流增量解帧成一个个 SSE data 载荷。

	只负责文本层：不认识 ``[DONE]``，也不认识 ``StreamChunk``。
	``feed`` 消费传输分块，``flush`` 在 EOF 时补交缺少最终换行的尾部事件。
	"""

	def __init__(self):

		self._buffer		: str		= ""
		self._data_lines	: List[str]	= []
		# 传输分块可以截断 UTF-8 码点，增量解码器会保留未完成字节直到下一块。
		# replace 保证流继续推进，但服务端非法字节可能使文本内容发生有损替换。
		self._decoder = codecs.getincrementaldecoder("utf-8")("replace")

	def feed(self, data: bytes) -> Iterator[str]:

		"""喂入一个传输分块，产出其中已经完整的 data 载荷。"""

		self._buffer += self._decoder.decode(data)

		while "\n" in self._buffer:
			line, self._buffer = self._buffer.split("\n", 1)
			event = self._consume_line(line)
			if event is not None:
				yield event

	def flush(self) -> Iterator[str]:

		"""EOF 收尾：补交最后一行以及尚未被空行分派的 data 载荷。

		这是给缺少最终换行的流用的，不是 ``[DONE]`` 的替代品。
		"""

		self._buffer += self._decoder.decode(b"", final=True)

		if self._buffer:
			line, self._buffer = self._buffer, ""
			event = self._consume_line(line)
			if event is not None:
				yield event

		event = self._take_pending()
		if event is not None:
			yield event

	def _consume_line(self, line: str) -> Optional[str]:

		"""处理一行，返回该行分派出的 data 载荷（没有则为 None）。"""

		line = line.rstrip("\r")

		# 空行是事件边界，把累积的 data 行分派出去。
		if line == "":
			return self._take_pending()

		if line.startswith("data:"):
			data = line[5:]
			if data.startswith(" "):
				data = data[1:]
			if data:
				self._data_lines.append(data)

		return None

	def _take_pending(self) -> Optional[str]:

		"""取出并清空累积的 data 行，没有累积时返回 None。"""

		if not self._data_lines:
			return None

		event = "\n".join(self._data_lines)
		self._data_lines.clear()
		return event


class StreamChunkParser:

	"""把 SSE data 载荷校验成 ``StreamChunk``，并维护连续失败预算。

	``parse`` 有三种返回：``DONE`` 表示流正常终止，``None`` 表示该事件在预算内
	被容忍并跳过，其余为校验通过的 ``StreamChunk``。
	"""

	def __init__(self, max_parse_errors: int = MAX_SSE_PARSE_ERRORS):

		self._max_parse_errors	= max_parse_errors
		self._parse_failures	= 0

	def parse(self, event: str) -> Any:

		if event == _DONE_PAYLOAD:
			return DONE

		try:
			chunk = StreamChunk.model_validate_json(event)

		except Exception as exception:
			self._parse_failures += 1
			logger.warning(
				"解析流式数据块失败 (%s/%s): %s",
				self._parse_failures,
				self._max_parse_errors,
				type(exception).__name__,
			)
			if self._parse_failures >= self._max_parse_errors:
				raise SSEParseError(
					f"连续 {self._parse_failures} 个 SSE 数据块无法解析"
				) from exception
			return None

		self._parse_failures = 0
		return chunk

