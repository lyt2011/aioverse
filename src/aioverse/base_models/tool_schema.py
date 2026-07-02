# 类型两件套
from pydantic import BaseModel, Field, model_serializer
from typing import List, Dict, Any, Optional


_Empty = object()


# 基础参数
class Argument(BaseModel):

	type		: str | List[str]
	description	: str
	default		: Any = _Empty
	
	@model_serializer(mode='wrap')
	def serialize(self, handler):
		
		data = handler(self)  # 先走默认序列化
		
		if self.default is not _Empty: data["default"] = self.default
		else: data.pop("default", None)
		
		return data

# 参数集
class Parameters(BaseModel):
	
	# 类型一般是object 不过不限 你爱填什么填什么
	type		: str = "object"
	properties	: Dict[str, Argument]
	required	: List[str]

# 函数
class Function(BaseModel):
	
	name		: str
	description	: str
	parameters	: Parameters

# 工具
class Tool(BaseModel):
	
	# openai默认是function
	type	: str = "function"
	function: Function