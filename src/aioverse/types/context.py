from typing import Dict, Any

from .content_array import ContentArray


class Context:
	
	__slots__ = [
		"role",
		"content"
	]
	
	def __init__(
		self,
		role	: str,
		content	: ContentArray | str
	):
	
		self.role		= role
		self.content	= content
	
	def __len__(self) -> int:
		
		return len(self.content)
	
	def toDict(self) -> Dict[str, Any]:
		
		"""直接调用content的toList方法即可"""
		
		if isinstance(self.content, ContentArray):
			
			# 字符串类型直接返回
			return {
				"role"		: self.role,
				"content"	: self.content.toList()
			}
		
		return {
			"role"		: self.role,
			"content"	: str(self.content)
		}