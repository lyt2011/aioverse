from .base_segment	import BaseSegment

from pydantic	import ConfigDict
from typing		import Any, Dict


class UnknownSegment(BaseSegment):
	
	"""未知类型消息段的兜底容器 保留原始数据透传"""
	
	model_config = ConfigDict(extra="allow")
	
	type: str # 不限制 Literal，接受任意 type
	
	def do_serialize(self) -> Dict[str, Any]:
		
		"""返回 type + 所有 extra 字段 不做格式转换"""
		
		result: Dict[str, Any] = {"type": self.type}
		
		# 收集所有未在模型中定义的 extra 字段
		for key, value in self.__pydantic_extra__.items() if self.__pydantic_extra__ else []:
			result[key] = value
		
		return result
