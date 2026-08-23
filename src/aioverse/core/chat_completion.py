from __future__ import annotations

from ..models		import Request, Response, StreamChunk
from ._transport	import _request_context, _stream_impl

import logging
import aiohttp

from typing import AsyncIterator


def chat_completion(
	request	: Request,
	session	: aiohttp.ClientSession,
) -> _ChatCompletion:

	"""
	发起一次请求，返回 ``_ChatCompletion`` 包装对象。

	可用 ``await`` 等待（非流式，返回 ``Response``），
	也可用 ``async for`` 迭代（流式，产出 ``StreamChunk``）。

	分流依据是响应头 ``content-type`` 是否为 ``text/event-stream``。
	只在发起一次请求；部分内容已经产出后的重试、去重和恢复需要由上层决定。
	"""

	return _ChatCompletion(request, session)


class _ChatCompletion:
	"""
	``chat_completion()`` 返回的包装对象。

	- ``await``  → 非流式，返回 ``Response``
	- ``async for`` → 流式，产出 ``StreamChunk``；非流式响应也兼容，产出单个 ``Response``
	"""

	def __init__(self, request: Request, session: aiohttp.ClientSession):
		
		self._request	= request
		self._session	= session
		self._iterator	= None

	def __await__(self):
		return self._resolve().__await__()

	async def _resolve(self) -> Response:
		
		async with _request_context(self._request, self._session) as response:
			response_text = await response.text()
		
		return Response.model_validate_json(response_text)

	def __aiter__(self) -> AsyncIterator[StreamChunk]:
		
		if self._iterator is None:
			self._iterator = self._stream().__aiter__()
		
		return self._iterator

	async def __anext__(self) -> StreamChunk:
		return await self.__aiter__().__anext__()

	async def aclose(self) -> None:
		
		if self._iterator is None:
			self._iterator = self._stream().__aiter__()
		
		await self._iterator.aclose()

	async def _stream(self) -> AsyncIterator[StreamChunk]:
		# 在类外定义（_transport._stream_impl），运行时赋值
		...


_ChatCompletion._stream = _stream_impl