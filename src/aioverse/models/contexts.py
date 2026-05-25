# 类型两件套
from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Any, Literal, Optional

# 多模态正文
from .contents import Segment
# AI返回的工具
from .tool_call_response import ToolCall


# 基础上下文模型
class Context(BaseModel):
	
	"""
	需要获取完整信息请通过模型自带的model_dump方法
	"""
	
	model_config = ConfigDict(slots=True)
	
	role	: str
	content	: Optional[List[Segment] | str] = None
	
	# 便于统计token
	token	: int = 0
	
	def __len__(self) -> int:
		
		# 优先使用token
		if self.token > 0: return self.token
		
		# 然后判断是否为None
		if not self.content: return 0
		
		# 判断self.content具体内容
		if isinstance(self.content, list):
			
			# 计算内部Segment的token
			return sum([
				len(content)
				for content in self.content
				if isinstance(content, Segment)
			])
		
		# 字符串则通过len计算
		if isinstance(self.content, str):
			
			# 这里*1是经过GPT-4分词器测试过多中文环境下的线性最佳值
			return len(self.content) * 1
		
		raise TypeError(f"content的类型不该为({type(self.content)})")
	
	def set_token(self, token: int):
		
		self.token = token
	
	def to_dict(self) -> Dict[str, Any]:
		
		"""
		基础的to_dict默认必须存在content
		不需要用到content的context需要重写该方法
		"""
		
		if self.content is None:
			
			raise ValueError("content必须拥有一个值")
		
		if isinstance(self.content, str):
			
			return {
				"role"		: self.role,
				"content"	: self.content
			}
		
		if isinstance(self.content, list):
			
			return {
				"role": self.role,
				"content": [
					content.to_dict()
					for content in self.content
					if isinstance(content, Segment) # 仅转类型为Segment的
				]
			}
		
		raise TypeError(f"content的类型({type(self.content)})是错误的")

# 提示词
class Prompt(Context):
	
	"""强制使用system 其他不用动"""
	
	role: Literal["system"] = "system"

# 对于工具调用请求的上下文 (ai返回)
class AssistantToolCalls(Context):
	
	# 强制role
	role		: Literal["assistant"] = "assistant"
	# 新增tool_calls
	tool_calls	: List[ToolCall]
	
	# 重写to_dict
	def to_dict(self) -> Dict[str, Any]:
		
		return {
			"role"		: self.role,
			"tool_calls": [
				tool.to_dict()
				for tool in self.tool_calls
			],
			"content"	: None # 强制None防篡改
		}

# 对于工具执行结果的上下文 单个结果
class ToolExecuteResult(Context):
	
	# 强制role为tool
	role		: Literal["tool"] = "tool"
	# 新增tool_call_id
	tool_call_id: str
	
	# 重写to_dict
	def to_dict(self) -> Dict[str, Any]:
		
		# 必须存在content(不为None)
		if self.content is None:
			
			raise ValueError("content的值不能为None")
		
		return {
			"role"			: self.role,
			"content"		: self.content, # 这里是工具的调用结果
			"tool_call_id"	: self.tool_call_id
		}