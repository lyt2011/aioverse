from .base_segment	import BaseSegment

from pydantic	import model_validator
from typing		import Literal, Optional, Any, Dict


class VideoInputSegment(BaseSegment):
	
	"""Base64 编码的视频输入消息段"""
	
	type	: Literal["input_video"]	= "input_video"
	data		: str
	format	: Optional[str]			= "mp4"
	
	@model_validator(mode="before")
	@classmethod
	def flatten_input_video_format(cls, data: Any) -> Any:
		
		"""
		兼容嵌套格式:
		{"type": "input_video", "input_video": {"data": "...", "format": "mp4"}}
		→ {"type": "input_video", "data": "...", "format": "mp4"}
		"""
		
		if isinstance(data, dict):
			inner = data.get("input_video")
			if isinstance(inner, dict):
				data = {
					**data,
					"data"	: inner.get("data", ""),
					"format": inner.get("format", "mp4")
				}
		
		return data
	
	def do_serialize(self) -> Dict[str, Any]:
		
		"""返回嵌套 Base64 视频格式。"""
		
		return {
			"type"		: self.type,
			self.type	: {
				"data"		: self.data,
				"format"	: self.format
			}
		}
