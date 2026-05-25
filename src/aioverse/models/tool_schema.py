# 类型两件套
from pydantic import BaseModel
from typing import List, Dict, Any


# 基础参数
class Argument(BaseModel):

	type		: str
	description	: str
	
	# 实现to_dict方法
	def to_dict(self) -> Dict[str, str]:
		
		return {
			"type"			: self.type,
			"description"	: self.description
		}

# 参数集
class Parameters(BaseModel):
	
	# 类型一般是object 不过不限 你爱填什么填什么
	type		: str = "object"
	properties	: Dict[str, Argument]
	required	: List[str]
	
	def to_dict(self) -> Dict[str, Any]:
		
		return {
			"type"		: self.type,
			"properties": {
				name: arg.to_dict()
				for name, arg in self.properties.items()
			},
			"required"	: self.required
		}

# 函数
class Function(BaseModel):
	
	name		: str
	description	: str
	parameters	: Parameters
	
	def to_dict(self) -> Dict[str, Any]:
		
		return {
			"name"			: self.name,
			"description"	: self.description,
			"parameters"	: self.parameters.to_dict()
		}

# 工具
class Tool(BaseModel):
	
	# openai默认是function
	type	: str = "function"
	function: Function
	
	def to_dict(self) -> Dict[str, Any]:
		
		return {
			"type"		: self.type,
			"function"	: self.function.to_dict()
		}