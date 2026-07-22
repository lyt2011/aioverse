from .base_segment	import BaseSegment

from pydantic	import model_validator
from typing		import Literal, Optional, Any, Dict


class FileSegment(BaseSegment):
	
	"""文件消息段"""
	
	type		: Literal["file"]			= "file"
	file_id		: str
	filename	: Optional[str]				= None
	file_size	: Optional[int]				= None
	
	@model_validator(mode="before")
	@classmethod
	def flatten_openai_format(cls, data: Any) -> Any:
		
		"""
		兼容 OpenAI 原始格式:
		{"type": "file", "file": {"file_id": "...", "filename": "...", "file_size": 123}}
		→ {"type": "file", "file_id": "...", "filename": "...", "file_size": 123}
		"""
		
		if isinstance(data, dict):
			inner = data.get("file")
			if isinstance(inner, dict):
				data = {
					**data,
					"file_id"	: inner.get("file_id", ""),
					"filename"	: inner.get("filename"),
					"file_size"	: inner.get("file_size")
				}
		
		return data
	
	def do_serialize(self) -> Dict[str, Any]:
		
		"""返回 OpenAI 兼容格式: {"type": "file", "file": {"file_id": "...", ...}}"""
		
		inner = {"file_id": self.file_id}
		if self.filename is not None:
			inner["filename"] = self.filename
		if self.file_size is not None:
			inner["file_size"] = self.file_size
		
		return {
			"type"	: "file",
			"file"	: inner
		}
