from typing import Dict, Any


class Content:
	
	"""
	openai协议中支持给content传入数组
	于是想到做这个
	"""
	
	__slots__ = ["content_type", "content_data"]
	
	def __init__(
		self,
		content_type: str,
		content_data: Any
	):
		
		self.content_type = content_type
		self.content_data = content_data
	
	def __len__(self) -> int:
		
		return len(str(self.content_data))
	
	def toDict(self) -> Dict[str, Any]:
		
		return {
			"type"				: self.content_type,
			self.content_type	: self.content_data
		}