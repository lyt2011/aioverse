# 类型注解
from typing import Dict, Any, Optional, Union
# json实现
import orjson


class JsonManager(dict):
	
	"""
	不做任何的错误处理
	全部抛给上级
	"""
	
	def __init__(self):
		
		super().__init__()
	
	def fromDict(
		self,
		dictionary: Dict[str, Any]
	) -> "self":
		
		self.update(dictionary)
		
		return self
	
	def fromString(
		self,
		string: str
	) -> "self":
		
		self.update(orjson.loads(string))
		
		return self
	
	def fromFile(
		self,
		path: str,
		**kwargs
	) -> "self":
		
		with open(
			path,
			encoding="utf-8",
			**kwargs
		) as file:
			
			self.fromString(file.read())
		
		return self
	
	def toDict(self) -> Dict[str, Any]:
		
		return self
	
	def toString(self) -> str:
		
		return orjson.dumps(str(self)).decode("utf-8")
	
	def hasKey(
		self,
		key: Any
	) -> bool:
		
		return key in self
	
	def setValue(
		self,
		key		: Any,
		value	: Any
	) -> None:
		
		self[key] = value
		
		return None
	
	def delValue(
		self,
		key: str
	) -> None:
		
		del self[key]
		
		return None
	
	def getValue(
		self,
		key		: Any,
		default	: Optional[Any] = None
	) -> Any:
		
		return self.get(key, default)