from pydantic	import BaseModel, Field
from typing		import Dict, List, Any, Optional, Self


class Request(BaseModel):
	
	"""
	一次 HTTP 请求的可变构建器。

	``timeout`` 覆盖 aiohttp 的完整请求生命周期；``stream_idle_timeout`` 仅限制
	流式请求等待下一个已解析数据块的时间，设为 None 时关闭该额外 watchdog。
	"""

	url					: str				= Field(..., description="需要请求的网址")
	timeout				: float				= Field(default=300, gt=0)
	stream_idle_timeout	: Optional[float]	= Field(default=60, gt=0)
	
	headers	: Dict[str, Any] = Field(default_factory=dict)
	body	: Dict[str, Any] = Field(default_factory=dict)
	params	: Dict[str, Any] = Field(default_factory=dict)
	
	@classmethod
	def build(cls, **kwargs) -> Self:
		return cls(**kwargs)
	
	def set_header(self, key: str, value: Any) -> Self:
		self.headers[key] = value
		return self
	def set_body(self, key: str, value: Any) -> Self:
		self.body[key] = value
		return self
	def set_param(self, key: str, value: Any) -> Self:
		self.params[key] = value
		return self