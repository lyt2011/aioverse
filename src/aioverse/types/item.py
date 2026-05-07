from typing import Optional, Any, Dict

import orjson


class Item:
	
	"""
	存放数据的物件
	一般用完就丢 用于函数之间的数据传输
	
	不支持动态的toDict
	"""
	
	def __init__(
		self,
		_default_result: Optional[Any] = None,
		**kwargs
	):
		
		# 默认返回值
		self._default_result	= _default_result
		
		for key, value in kwargs.items():
			
			# 判断是否可能为关键方法
			if key.startswith("__") and key.endswith("__"):
				
				raise TypeError(f"不可修改关键方法 ({key})")
			
			setattr(self, key, value)
		
		# 这个kwargs便于转字典
		self._kwargs			= kwargs
	
	def __getattr__(self, name: str) -> None:
		
		"""
		这里直接返回none
		因为能运行这个函数证明已经是不存在了
		"""
		
		return self._default_result
	
	def toDict(self) -> Dict[str, Any]:
		
		return self._kwargs
	
	def toString(self) -> str:
		
		return orjson.dumps(self.toDict()).decode("utf-8")