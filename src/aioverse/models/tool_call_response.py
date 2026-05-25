# 这里是openai格式的工具调用请求的数据模型
# tool.py是请求模型 这里是响应模型 不要搞混

# 类型两件套
from pydantic import BaseModel, model_validator
from typing import List, Dict, Any

# json实现
import orjson


class Function(BaseModel):
	
	name		: str
	arguments	: Dict[str, Any]
	
	@model_validator(mode="before")
	@classmethod
	def verify_arguments(
		cls,
		data: Dict[str, Any]
	) -> Dict[str, Any]:
		
		arguments = data.get("arguments")
		
		if isinstance(arguments, str)		: data["arguments"] = orjson.loads(arguments)
		elif not isinstance(arguments, dict): raise TypeError(f"arguments的类型不能为{type(arguments)}")
		
		return data
	
	def to_dict(self) -> Dict[str, Any]:
		
		return {
			"name"		: self.name,
			"arguments"	: orjson.dumps(self.arguments).decode()
		}

# 单个工具请求
class ToolCall(BaseModel):

	id		: str
	type	: str
	function: Function
	
	def to_dict(self) -> Dict[str, Any]:
		
		return {
			"id"		: self.id,
			"type"		: self.type,
			"function"	: self.function.to_dict()
		}