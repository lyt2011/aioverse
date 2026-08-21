from .errors		import ResponseCodeError, SSEParseError
from .models		import (
	Response,
	Request,
	BaseContext,
	StreamChunk
)

import asyncio
import codecs
import logging
import aiohttp
import json

from typing import Any, List, Optional, AsyncIterator

logger = logging.getLogger(__name__)

# 这是单条流内的容错预算，不是 HTTP 重试次数；成功解析一个 chunk 会重置连续失败计数。
MAX_SSE_PARSE_ERRORS = 3
# [DONE] 是 OpenAI 风格的控制载荷，不是可验证的 StreamChunk；用私有哨兵
# 与 None（忽略的事件）和正常 chunk 区分开来。
_SSE_DONE = object()


class OpenAIClient:

	"""基于调用方提供的 ClientSession 执行 OpenAI 兼容请求。

	ClientSession 归调用方所有，本类只通过上下文管理器释放单次 HTTP 响应。
	``call_stream`` 只发起一次请求；部分内容已经产出后的重试、去重和恢复
	需要由上层决定，避免隐式重放模型输出。
	"""

	def __init__(
		self, *, 
		session: Optional[aiohttp.ClientSession]	= None
	):
		
		# 手动控制或运行时创建
		self.session = session
	
	def _get_session(self) -> aiohttp.ClientSession:
		return self.session or aiohttp.ClientSession()
	
	async def _iter_sse_chunks(self, response: aiohttp.ClientResponse) -> AsyncIterator[StreamChunk]:
		buffer = ""
		data_lines: list[str] = []
		parse_failures = 0
		# 传输分块可以截断 UTF-8 码点，增量解码器会保留未完成字节直到下一块。
		# replace 保证流继续推进，但服务端非法字节可能使文本内容发生有损替换。
		decoder = codecs.getincrementaldecoder("utf-8")("replace")

		def parse_event(data: str) -> Any:
			nonlocal parse_failures

			if data == "[DONE]":
				return _SSE_DONE

			try:
				chunk = StreamChunk.model_validate_json(data)
			except Exception as exception:
				parse_failures += 1
				logger.warning(
					"解析流式数据块失败 (%s/%s): %s",
					parse_failures,
					MAX_SSE_PARSE_ERRORS,
					type(exception).__name__,
				)
				if parse_failures >= MAX_SSE_PARSE_ERRORS:
					raise SSEParseError(
						f"连续 {parse_failures} 个 SSE 数据块无法解析"
					) from exception
				return None

			parse_failures = 0
			return chunk

		async def process_line(line: str):
			line = line.rstrip("\r")
			if line == "":
				if not data_lines:
					return None
				data = "\n".join(data_lines)
				data_lines.clear()
				return parse_event(data)

			# 这里只实现 OpenAI 使用的 data-only SSE 子集：空行分派事件，
			# 多个 data 行按 LF 拼接；event/id/retry 字段不参与请求恢复。
			if line.startswith("data:"):
				data = line[5:]
				if data.startswith(" "):
					data = data[1:]
				if data:
					data_lines.append(data)
			return None

		async for chunk_bytes in response.content.iter_chunked(1024):
			buffer += decoder.decode(chunk_bytes)

			while "\n" in buffer:
				line, buffer = buffer.split("\n", 1)
				parsed = await process_line(line)
				if parsed is _SSE_DONE:
					logger.info("流式请求完成 [DONE]")
					return
				if parsed is not None:
					yield parsed

		# EOF 允许补交缺少最终换行的最后一个 data 事件；它不是 [DONE] 的替代品。
		buffer += decoder.decode(b"", final=True)
		if buffer:
			parsed = await process_line(buffer)
			if parsed is _SSE_DONE:
				logger.info("流式请求完成 [DONE]")
				return
			if parsed is not None:
				yield parsed

		if data_lines:
			parsed = parse_event("\n".join(data_lines))
			data_lines.clear()
			if parsed is _SSE_DONE:
				logger.info("流式请求完成 [DONE]")
				return
			if parsed is not None:
				yield parsed
	
	
	async def call(self, request: Request) -> Response:
		
		session = self._get_session()
		
		async with session.post(
			url		= request.url,
			headers	= request.headers,
			params	= request.params,
			json	= request.body,
			timeout = request.timeout
		) as response:
			response_code = response.status
			response_text = await response.text()
		
		logger.info(f"请求完成: {response_code}")
		
		# HTTP 成功和模型 schema 合法是两层约束：200 响应仍会经过 Response 校验。
		if response_code != 200:
			try:
				response_data = json.loads(response_text)
			except (TypeError, ValueError):
				response_data = response_text
			raise ResponseCodeError(code=response_code, response=response_data)
		
		return Response.model_validate_json(response_text)
	
	
	async def call_stream(self, request: Request) -> AsyncIterator[StreamChunk]:
		
		session = self._get_session()
		
		async with session.post(
			url		= request.url,
			headers	= request.headers,
			params	= request.params,
			json	= request.body,
			timeout = request.timeout
		) as response:
			
			if response.status != 200:
				
				response_text = await response.text()
				
				try:
					response_data = json.loads(response_text)
				
				except (TypeError, ValueError):
					response_data = response_text
				
				raise ResponseCodeError(code=response.status, response=response_data)
			
			chunk_iterator = None
			
			try:
				
				chunk_iterator	= self._iter_sse_chunks(response).__aiter__()
				idle_timeout	= request.stream_idle_timeout

				while True:
					try:
						
						if idle_timeout is None:
							chunk = await chunk_iterator.__anext__()
						else:
							# 空闲计时的是下一个已解析 StreamChunk，而不是原始 socket 字节；
							# 心跳、注释和不完整事件不会重置该上层 watchdog。
							chunk = await asyncio.wait_for(
								chunk_iterator.__anext__(),
								timeout=idle_timeout,
							)
					
					except StopAsyncIteration:
						break
					
					except asyncio.TimeoutError as exception:
						raise asyncio.TimeoutError(f"流式响应在 {idle_timeout} 秒内没有产生下一个数据块") from exception

					yield chunk
			
			except GeneratorExit:
				logger.info("流式请求被中断 (stop)")
				raise
			
			else:
				logger.info("流式请求完成 (连接关闭)")
			
			finally:
				
				# 提前停止消费时也要关闭内层生成器，确保 response 上下文退出前释放解析状态。
				if chunk_iterator is not None:
					aclose = getattr(chunk_iterator, "aclose", None)
					if callable(aclose):
						await aclose()
