# 类型注解
from typing import Optional, Any, Dict

# json实现
import orjson


class Item:
	
	"""
	一般用于函数之间的数据传输
	"""
	
	__slots__ = (
		"_default",
		"_mapping"
	)
	
	def __init__(
		self,
		default: Optional[Any] = None,
		**kwargs
	):
		
		# 设置默认返回值
		object.__setattr__(self, "_default", default)
		# 设置映射表
		object.__setattr__(self, "_mapping", kwargs)
		
	
	def __setattr__(self, key: str, value: Any):
		
		# 过滤__slots__
		if key == "_mapping":
			
			raise RuntimeError("不可修改映射表")
		
		elif key == "_default":
			
			object.__setattr__(self, key, value)
		
		else:
			
			self._mapping[key] = value
		
		return None
	
	def __getattr__(self, name: str) -> Any:
		
		return self._mapping.get(name, self._default)
	
	def to_dict(self) -> Dict[str, Any]:
		
		return self._mapping.copy()
	
	def to_string(self) -> str:
		
		return orjson.dumps(self._mapping).decode("utf-8")