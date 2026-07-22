from .base_segment	import BaseSegment

from pydantic	import model_validator
from typing		import Literal, Optional, Any, Dict


class AudioInputSegment(BaseSegment):
	
	"""音频输入消息段"""
	
	type	: Literal["input_audio"]	= "input_audio"
	format	: Optional[str]				= "mp3"
	data	: str											# base64 编码的音频数据
	
	@model_validator(mode="before")
	@classmethod
	def flatten_openai_format(cls, data: Any) -> Any:
		
		"""
		兼容 OpenAI 原始格式:
		{"type": "input_audio", "input_audio": {"data": "...", "format": "mp3"}}
		→ {"type": "input_audio", "data": "...", "format": "mp3"}
		"""
		
		if isinstance(data, dict):
			inner = data.get("input_audio")
			if isinstance(inner, dict):
				data = {**data, "data": inner.get("data", ""), "format": inner.get("format", "mp3")}
		
		return data
	
	def do_serialize(self) -> Dict[str, Any]:
		
		"""返回 OpenAI 兼容格式: {"type": "input_audio", "input_audio": {"data": "...", "format": "mp3"}}"""
		
		return {
			"type"			: self.type,
			self.type		: {
				"data"		: self.data,
				"format"	: self.format
			}
		}
