from .base_segment	import BaseSegment

from pydantic	import model_validator
from typing		import Literal, Optional, Any, Dict


class ImageUrlSegment(BaseSegment):
	
	"""图片消息段"""
	
	type	: Literal["image_url"]								= "image_url"
	url		: str
	detail	: Optional[Literal["auto", "low", "high"]]			= "auto"
	
	@model_validator(mode="before")
	@classmethod
	def flatten_openai_format(cls, data: Any) -> Any:
		
		"""
		兼容 OpenAI 原始格式:
		{"type": "image_url", "image_url": {"url": "...", "detail": "auto"}}
		→ {"type": "image_url", "url": "...", "detail": "auto"}
		"""
		
		if isinstance(data, dict):
			inner = data.get("image_url")
			if isinstance(inner, dict):
				data = {**data, "url": inner.get("url", ""), "detail": inner.get("detail", "auto")}
		
		return data
	
	def do_serialize(self) -> Dict[str, Any]:
		
		"""返回 OpenAI 兼容格式: {"type": "image_url", "image_url": {"url": "...", "detail": "auto"}}"""
		
		return {
			"type"		: "image_url",
			"image_url"	: {
				"url"	: self.url,
				"detail": self.detail
			}
		}
