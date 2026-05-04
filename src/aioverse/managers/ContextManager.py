# 类型注解
from typing import List, Dict
# 深度复制
from copy import deepcopy
# 抽象接口
from aioverse.models.protocols import ContextManagerProtocol

# 上下文对象+提示词对象
from aioverse.models.structs import Prompt, Context


class ContextManager(ContextManagerProtocol):
	
	"""管理上下文"""
	
	def __init__(
		self,
		context: List[Context] = None
	):
		
		self._context = context if context else []
	
	# len()
	def __len__(self) -> int : return len(self._context)
	
	# str()
	def __repr__(self) -> str:
		
		chatHistory = [
			f"{context.role}: {context.content}"
			for context in self._context
		]
		
		return "\n".join(chatHistory)
	
	# 清空上下文
	def clear(self) -> None:
		
		self._context.clear()
		
		return None
	
	# 是否含有提示词
	def hasPrompt(self) -> bool:
		
		"""是否添加了提示词 返回bool"""
		
		if not self._context: return False
		
		# 判断是否已有提示词
		return self._context[0].role == "system"
	
	# 强行修改提示词
	def setPrompt(
		self,
		prompt: Prompt
	) -> None:
		
		"""
		强制设置提示词
		提示词存在则更改
		不存在则添加
		"""
			
		# 判断是否已含有提示词
		if self.hasPrompt():
			
			# 直接替换
			self._context[0] = prompt
		
		# 否则就插入
		else: self._context.insert(0, prompt)
		
		return None
	
	# 获取提示词
	def getPrompt(self) -> Prompt | None:
		
		return self._context[0] if self.hasPrompt() else None
	
	# 删除最后一个上下文
	def deleteLastContext(self) -> None:
		
		self._context.pop()
		
		return None

	# 添加单个上下文
	def addContext(
		self,
		context: Context
	) -> None:
		
		"""向self._context添加单个上下文"""
		
		if (
			self.hasPrompt()
			and context.role == "system"
		):
			
			raise RuntimeError(
				"不能在已有提示词的上下文管理中"
				"再次通过addContext添加提示词"
				"，如需修改请使用setPrompt"
			)
		
		self._context.append(context)
		
		return None
	
	# 获取上下文副本
	def toList(self) -> List[
		Dict[str, str]
	]:
		
		# 转换上下文
		return [
			context.toDict()
			for context in self._context
			if isinstance(context, (Context, Prompt)) # 为Context的实例时转换
		]
	
	def isOut(
		self,
		maxTokens: int
	) -> bool:
		
		# 遍历聊天记录 获取所有的文本
		fullContent = [
			str(context.content).encode("utf-8")
			for context in self._context
		]
		
		# 计算token
		totalToken = len(b"".join(fullContent))
		
		# 返回超限结果
		return totalToken // 2 > maxTokens
	
	def trim(self) -> None:
		
		# 根据实际情况删除上下文
		if self.hasPrompt():
				
			# 删第二个
			self._context.pop(1)
			
		else: self._context.pop(0)
		
		return None