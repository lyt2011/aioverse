from typing import Dict, Any, Optional

from .content_array import ContentArray


class Context:
	
	__slots__ = [
		"role",
		"content",
		"token"
	]
	
	def __init__(
		self,
		role	: str,
		content	: ContentArray | str,
		token	: Optional[int] = None
	):
	
		self.role		= role
		self.content	= content
		self.token		= token
	
	def __len__(self) -> int:
		
		return (
			len(self.content) if not self.token
			else self.token
		)
	
	def setToken(
		self,
		count: int
	) -> None:
		
		self.token = count
		
		return None
	
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
	
	# 获取完整实例数据 (用于上下文持久化)
	def to_raw_dict(self) -> Dict[str, Any]:
		
		return {
			"token": self.token,
			**self.toDict()
		}
	
	@classmethod
	def from_dict(cls, data: Dict[str, Any]) -> "Context":
		
		"""
		为保证兼容性 data的值将直接被当做content参数以实例化Context
		"""
		
		return cls(**data)