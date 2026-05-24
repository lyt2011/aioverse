# 类型注解
from typing import List, Dict
# 深度复制
from copy import deepcopy

# 上下文对象+提示词对象
from aioverse.types import Prompt, Context, Content


class ContextManager:
	
	"""管理上下文"""
	
	__slots__ = [
		"_contexts",
		"_token"
	]
	
	def __init__(
		self,
		context_array	: List[Context] = None,
		token			: int			= 0
	):
		
		self._contexts	= context_array if context_array else []
		self._token		= token
	
	# len()
	def __len__(self) -> int:
		
		"""这个是用于计算对话次数的"""
		return len(self._contexts)
	
	# str()
	def __repr__(self) -> str:
		
		chat_history = [
			f"{context.role}: {context.content}"
			for context in self._contexts
		]
		
		return "\n".join(chat_history)
	
	@property
	def token(self) -> int:
		
		"""
		如果自定义token小于等于0
		返回估算的token(全部字符*1.21)
		
		否则直接返回自定义的token数
		"""
		
		if self._token <= 0:
			
			return sum([
				len(context)
				for context in self._contexts
			]) * 1.21
		
		return self._token
	
	def set_token(
		self,
		token: int
	) -> None:
		
		self._token = token
	
	# 清空上下文
	def clear(
		self,
		keep_prompt: bool = False
	) -> None:
		
		"""
		Q: 为什么保留提示词时不使用self.trim()清理
		A: 因为用self.trim()每次都得self.hasPrompt()，开销大，而这样我只需要写一次
		"""
	
		# 保留提示词且有提示词
		if keep_prompt and self.has_prompt():
			
			# 遍历提示词之后的元素 清理
			for context in self._contexts[1:]: self._contexts.remove(context)
		
		# 否则直接全清
		else:
			
			self._contexts.clear()
		
		return None
	
	# 是否含有提示词
	def has_prompt(self) -> bool:
		
		"""是否添加了提示词 返回bool"""
		
		# 过滤边界情况
		if not (
			self._contexts
			or isinstance(self._contexts, Context)
		): return False
		
		# 取第一个 (OpenAI格式)
		return self._contexts[0].role == "system"
	
	# 强行修改提示词
	def set_prompt(
		self,
		prompt: Prompt | Context
	) -> None:
		
		"""
		强制设置提示词
		提示词存在则更改
		不存在则添加
		"""
			
		# 判断是否已含有提示词
		if self.has_prompt():
			
			# 直接替换
			self._contexts[0] = prompt
		
		# 否则就插入
		else: self._contexts.insert(0, prompt)
		
		return None
	
	# 获取提示词
	def get_prompt(self) -> Prompt | None:
		
		return self._contexts[0] if self.hasPrompt() else None
	
	# 删除最后一个上下文
	def delete_last_context(self) -> None:
		
		self._contexts.pop()
		
		return None

	# 添加单个上下文
	def add_context(
		self,
		context: Context
	) -> None:
		
		"""向self._contexts添加单个上下文"""
		
		if (
			self.has_prompt()
			and context.role == "system"
		):
			
			raise RuntimeError(
				"不能在已有提示词的上下文管理中"
				"再次通过addContext添加提示词"
				"，如需修改请使用setPrompt"
			)
		
		self._contexts.append(context)
		
		return None
	
	# 获取上下文副本
	def to_list(
		self,
		return_prompt: bool = True
	) -> List[Dict[str, str]]:
		
		# 设置返回类型
		return_type = (
			Context if not return_prompt
			else (Context, Prompt)
		)
		
		# 转换上下文
		return [
			context.to_dict()
			for context in self._contexts
			if isinstance(context, return_type)
		]
	
	# 获取self._contexts
	def get_list(self) -> List[Context]:
		
		return self._contexts
	
	def is_out_of(
		self,
		max_tokens: int
	) -> bool:
		
		"""
		比较实际token与最大token
		当前token大于等于返回True
		"""
		
		# 对比大小 返回布尔
		return self.token >= max_tokens
	
	def trim(self) -> None:
		
		# 根据实际情况删除上下文
		if self.hasPrompt():
				
			# 删第二个
			self._contexts.pop(1)
			
		else: self._contexts.pop(0)
		
		return None