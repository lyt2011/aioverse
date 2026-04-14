
"""
专门为ai设计的类型注解
便于解析

注意
	不能用于isinstance判断 因为这不是真的类型
	仅用于AITools的类型注解 便于转换为字符串
	不建议用于其他代码的类型注解 idle/类型检查工具无法正确识别
"""

class Meta(type):
	
	def __repr__(cls): return cls.__name__.lower()

class List:
	
	def __class_getitem__(cls, item: str) -> str:
		
		return f"List[{item}]"

class Dict:
	
	def __class_getitem__(cls, item: tuple) -> str:
		
		key, value = item
		
		return f"Dict[{key}: {value}]"

class Union:
	
	def __class_getitem__(cls, item: tuple) -> str:
		
		v1, v2 = item
		
		return f"Union[{v1} or {v2}]"

class Optional:
	
	def __class_getitem__(cls, item: str) -> str:
	
		return Union[item, None]

class String(metaclass=Meta)	: pass
class Int(metaclass=Meta)		: pass
class Float(metaclass=Meta)		: pass
class Bool(metaclass=Meta)		: pass