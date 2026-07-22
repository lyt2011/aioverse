from pydantic	import BaseModel, model_serializer
from typing		import Dict, Any

import orjson


class BaseSegment(BaseModel):
	
	"""多模态消息段的抽象基类 子类必须实现 _serialize()"""
	
	type: str
	
	@model_serializer(mode="wrap")
	def _serialize(self, serializer, info) -> Dict[str, Any]:
		
		"""
		利用 Pydantic 序列化钩子 确保嵌套在 Context 中也能正确输出
		子类必须重写 do_serialize() 来定义具体的多模态结构
		"""
		
		return self.do_serialize()
	
	def do_serialize(self) -> Dict[str, Any]:
		
		"""子类必须重写此方法 定义具体 API 格式"""
		
		raise NotImplementedError("子类必须实现 do_serialize() 以适配目标 API 的多模态格式")
	
	def model_dump(self, **kwargs) -> Dict[str, Any]:
		
		"""兼容直接调用 model_dump() 的场景"""
		
		return self.do_serialize()
	
	def model_dump_json(self, **kwargs) -> str:
		
		"""重写序列化JSON方法"""
		
		return orjson.dumps(self.do_serialize()).decode()
