# 类型注解
from typing import List, Dict
# 深度复制
from copy import deepcopy
# 抽象接口
from aioverse.models.protocols import ContextManagerProtocol


class ContextManager(ContextManagerProtocol):
	
	"""管理上下文"""
	
	def __init__(
		self,
		context: List[ Dict[str, str] ] = None
	):
		
		self._context = context if context else []
	
	# len()
	def __len__(self) -> int : return len(self._context)
	
	# str()
	def __repr__(self) -> str:
		
		_chatData = []
		
		for context in self._context:
			
			_chatData.append(
				f"{context['role']}: "
				f"{context['content']}"
			)
		
		return "\n".join(_chatData)
	
	# 清空上下文
	def clear(self) -> None:
		
		self._context.clear()
		
		return None
	
	# 是否含有提示词
	def hasPrompt(self) -> bool:
		
		"""是否添加了提示词 返回bool"""
		
		if not self._context: return False
		
		# 判断是否已有提示词
		return self._context[0].get("role") == "system"
	
	# 强行修改提示词
	def setPrompt(
		self,
		prompt: str
	) -> None:
		
		"""
		强制设置提示词
		提示词存在则更改
		不存在则添加
		"""
		
		# 生成提示词字典
		promptDict = {
			"role"   : f"system",
			"content": f"{prompt}"
		}
		
		# 处理没有上下文的情况
		if not self._context:
			
			# 没有上下文可直接添加
			self._context.append(promptDict)
		
		else:
			
			# 获取提示词的角色名 并判断是否为提示词
			if self._context[0].get("role") == "system":
				
				# 直接替换 生成了不用白不用😱😱😱
				self._context[0] = promptDict
			
			# 否则就插入
			else: self._context.insert(0, promptDict)
		
		return None
	
	# 删除最后一个上下文
	def deleteLastContext(self) -> None:
		
		self._context.pop()
		
		return None

	# 添加单个上下文
	def addContext(
		self,
		context: Dict[str, str]
	) -> None:
		
		"""向self._context添加单个上下文"""
		
		if not isinstance(context, dict):
			
			raise ValueError(f"context上下文不能为 {type(context)}")
		
		if (
			not "role"    in context or
			not "content" in context
		):
			
			raise ValueError(
				f"传入的上下文不含有r"
				f"ole或content键 {context.keys()}"
			)
		
		self._context.append(context)
		
		return None
	
	# 获取上下文副本
	def toList(self) -> List[
		Dict[str, str]
	]:
		
		return deepcopy(self._context) # 防篡改