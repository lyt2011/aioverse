"""内部传输辅助：请求上下文、SSE 块迭代、空闲超时与流式实现。

``chat_completion`` 模块只保留公开入口 ``chat_completion`` 与包装类
``_ChatCompletion``，以下划线命名的传输细节全部收拢到这里。其中的
``iter_stream_chunks`` 虽不带下划线，但属于底层流解析原语，由 ``core``
包直接重新导出。
"""

from __future__ import annotations

from ..errors	import ResponseCodeError
from ..models	import Request, Response, StreamChunk

from .sse	import DONE, READ_CHUNK_SIZE, SSEDecoder, StreamChunkParser

import asyncio
import logging
import aiohttp

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, AsyncIterator, Optional


if TYPE_CHECKING:
	from .chat_completion	import _ChatCompletion


logger = logging.getLogger(__name__)

_STREAM_CONTENT_TYPES = ("text/event-stream",)


@asynccontextmanager
async def _request_context(
	request	: Request,
	session	: aiohttp.ClientSession,
) -> AsyncIterator[aiohttp.ClientResponse]:

	"""
	发送 POST 请求并持有响应连接
	非 200 时先读完响应体再抛错，连接由上下文管理器统一释放
	"""

	async with session.post(
		url		= request.url,
		headers	= request.headers,
		params	= request.params,
		json	= request.body,
		timeout	= request.timeout,
	) as response:

		if response.status != 200:
			raise ResponseCodeError(
				code		= response.status,
				response	= await response.text(),
			)

		yield response


async def iter_stream_chunks(response: aiohttp.ClientResponse) -> AsyncIterator[StreamChunk]:

	"""
	把 HTTP 响应体读成 ``StreamChunk`` 序列
	遇到 ``[DONE]`` 立即结束；EOF 时会补交缺少最终换行的尾部事件
	"""

	decoder	= SSEDecoder()
	parser	= StreamChunkParser()

	async for data in response.content.iter_chunked(READ_CHUNK_SIZE):
		for event in decoder.feed(data):

			chunk = parser.parse(event)

			if chunk is DONE:
				logger.info("流式请求完成 [DONE]")
				return

			if chunk is not None:
				yield chunk

	for event in decoder.flush():

		chunk = parser.parse(event)

		if chunk is DONE:
			logger.info("流式请求完成 [DONE]")
			return

		if chunk is not None:
			yield chunk


async def _iter_with_idle_timeout(
	chunks			: AsyncIterator[StreamChunk],
	idle_timeout	: Optional[float],
) -> AsyncIterator[StreamChunk]:

	"""
	给每次取块加上空闲上限

	空闲计时的是下一个已解析 ``StreamChunk``，而不是原始 socket 字节；
	心跳、注释和不完整事件不会重置该上层 watchdog
	"""

	iterator = chunks.__aiter__()

	try:
		while True:
			try:

				if idle_timeout is None:
					chunk = await iterator.__anext__()
				else:
					chunk = await asyncio.wait_for(
						iterator.__anext__(),
						timeout = idle_timeout,
					)

			except StopAsyncIteration:
				return

			except asyncio.TimeoutError as error:
				raise asyncio.TimeoutError(f"流式响应在 {idle_timeout} 秒内没有产生下一个数据块") from error

			yield chunk

	finally:
		# 提前停止消费时也要关闭内层生成器，确保 response 上下文退出前释放解析状态。
		aclose = getattr(iterator, "aclose", None)
		if callable(aclose):
			await aclose()


async def _stream_impl(self: _ChatCompletion) -> AsyncIterator[StreamChunk]:
	
	async with _request_context(self._request, self._session) as response:

		ct = response.headers.get("content-type", "")
		
		if ct.startswith(_STREAM_CONTENT_TYPES):

			chunks = _iter_with_idle_timeout(iter_stream_chunks(response), self._request.stream_idle_timeout)

			try:
				async for chunk in chunks:
					yield chunk

			except GeneratorExit:
				logger.info("流式请求被中断 (stop)")
				raise

			else:
				logger.info("流式请求完成 (连接关闭)")

			finally:
				await chunks.aclose()

		else:

			response_text = await response.text()
			logger.info("请求完成: %s", response.status)
			yield Response.model_validate_json(response_text)