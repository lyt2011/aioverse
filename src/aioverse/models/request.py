from pydantic	import BaseModel, Field, PrivateAttr
from typing		import Dict, List, Any, Optional, Self


class Request(BaseModel):
	"""一次 HTTP 请求的可变构建器。

	``timeout`` 覆盖 aiohttp 的完整请求生命周期；``stream_idle_timeout`` 仅限制
	流式请求等待下一个已解析数据块的时间，设为 None 时关闭该额外 watchdog。
	"""

	url				: str = Field(..., description="需要请求的网址")
	timeout			: float = Field(default=300, gt=0)
	stream_idle_timeout	: Optional[float] = Field(default=60, gt=0)
	
	_headers: Dict[str, Any] = PrivateAttr(default_factory=dict)
	_body	: Dict[str, Any] = PrivateAttr(default_factory=dict)
	_params	: Dict[str, Any] = PrivateAttr(default_factory=dict)
	
	def set_header(self, key: str, value: Any) -> Self:
		self._headers[key] = value
		return self
	def set_body(self, key: str, value: Any) -> Self:
		self._body[key] = value
		return self
	def set_param(self, key: str, value: Any) -> Self:
		self._params[key] = value
		return self
	
	@property
	def headers(self):
		return self._headers
	@property
	def body(self):
		return self._body
	@property
	def params(self):
		return self._params
