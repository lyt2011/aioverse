from typing import Dict, Any


class Content:
	
	"""
	openai协议中支持给content传入数组
	于是想到做这个
	"""
	
	__slots__ = ["_type", "data"]
	
	def __init__(
		self,
		type: str,
		data: Any
	):
		
		self._type	= type
		self.data	= data
	
	def __len__(self) -> int:
		
		return len(str(self.data))
	
	def toDict(self) -> Dict[str, Any]:
		
		return {
			"type"		: self._type,
			self._type	: self.data
		}
	
	@classmethod
	def from_dict(cls, data: Dict[str, Any]) -> "Content":
		
		# 先获取类型
		_type	= data["type"]
		# 通过类型获取数据
		data	= data[_type]
		
		return cls(type=_type, data=data)