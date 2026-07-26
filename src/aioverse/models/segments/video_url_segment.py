from .base_segment	import BaseSegment

from pydantic	import model_validator
from typing		import Literal, Optional, Any, Dict


class VideoUrlSegment(BaseSegment):
	
	"""URL 视频输入消息段"""
	
	type	: Literal["video_url"]	= "video_url"
	url		: str
	format	: Optional[str]			= None
	
	@model_validator(mode="before")
	@classmethod
	def flatten_video_url_format(cls, data: Any) -> Any:
		
		"""
		兼容嵌套格式:
		{"type": "video_url", "video_url": {"url": "..."}}
		→ {"type": "video_url", "url": "..."}
		"""
		
		if isinstance(data, dict):
			inner = data.get("video_url")
			if isinstance(inner, dict):
				data = {
					**data,
					"url"	: inner.get("url", ""),
					"format": inner.get("format")
				}
		
		return data
	
	def do_serialize(self) -> Dict[str, Any]:
		
		"""返回嵌套视频 URL 格式。"""
		
		video_url = {"url": self.url}
		if self.format is not None:
			video_url["format"] = self.format
		
		return {
			"type"		: self.type,
			self.type	: video_url
		}
