from .base_segment	import BaseSegment

from pydantic	import model_validator
from typing		import Literal, Optional, Any, Dict


class AudioUrlSegment(BaseSegment):
	
	"""URL 音频输入消息段"""
	
	type	: Literal["audio_url"]	= "audio_url"
	url		: str
	format	: Optional[str]			= None
	
	@model_validator(mode="before")
	@classmethod
	def flatten_audio_url_format(cls, data: Any) -> Any:
		
		"""
		兼容嵌套格式:
		{"type": "audio_url", "audio_url": {"url": "..."}}
		→ {"type": "audio_url", "url": "..."}
		"""
		
		if isinstance(data, dict):
			inner = data.get("audio_url")
			if isinstance(inner, dict):
				data = {
					**data,
					"url"	: inner.get("url", ""),
					"format": inner.get("format")
				}
		
		return data
	
	def do_serialize(self) -> Dict[str, Any]:
		
		"""返回嵌套音频 URL 格式。"""
		
		audio_url = {"url": self.url}
		if self.format is not None:
			audio_url["format"] = self.format
		
		return {
			"type"		: self.type,
			self.type	: audio_url
		}
