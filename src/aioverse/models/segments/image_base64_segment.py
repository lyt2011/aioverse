from .base_segment	import BaseSegment

from pydantic	import model_validator
from typing		import Literal, Optional, Any, Dict


class ImageBase64Segment(BaseSegment):
	
	"""Base64 编码的图片消息段 (区别于 ImageUrlSegment 的 URL 方式)"""
	
	type		: Literal["image"]			= "image"
	data		: str											# base64 编码的图片数据
	media_type	: Optional[str]				= "image/png"		# MIME 类型
	
	@model_validator(mode="before")
	@classmethod
	def flatten_openai_format(cls, data: Any) -> Any:
		
		"""
		兼容 OpenAI 原始格式:
		{"type": "image", "image": {"data": "...", "media_type": "image/png"}}
		→ {"type": "image", "data": "...", "media_type": "image/png"}
		"""
		
		if isinstance(data, dict):
			inner = data.get("image")
			if isinstance(inner, dict):
				data = {
					**data,
					"data"		: inner.get("data", ""),
					"media_type": inner.get("media_type", "image/png")
				}
		
		return data
	
	def do_serialize(self) -> Dict[str, Any]:
		
		"""返回 OpenAI 兼容格式: {"type": "image", "image": {"data": "...", "media_type": "image/png"}}"""
		
		return {
			"type"	: "image",
			"image"	: {
				"data"		: self.data,
				"media_type": self.media_type
			}
		}
