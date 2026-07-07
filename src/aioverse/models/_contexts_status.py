from pydantic	import BaseModel, Field, SerializeAsAny, PrivateAttr
from typing		import List, Union, Optional

from .contexts		import Context
from .blocks		import ToolCallingBlock, ContextsBlock
from ..protocols	import ContextsBlockProtocol


SUPPORT_CONTEXT_TYPE = Union[Context, ToolCallingBlock, ContextsBlock]


class _ContextsStatus(BaseModel):
	
	"""上下文的内部状态 (提供给ContextManager使用)"""
	
	contexts: List[SUPPORT_CONTEXT_TYPE] = Field(default_factory=list)
	prompt	: Optional[Context] = Field(default=None)
	
	token	: int	= Field(default=0)
	
	_is_dirty		: bool = PrivateAttr(default=True)
	_contexts_cache	: List[Context] = PrivateAttr(default_factory=list)
	
	def is_dirty(self) -> bool:
		return self._is_dirty
	
	def set_dirty(self):
		self._is_dirty = True
	def set_token(self, token: int):
		self.token = token
	def set_prompt(self, prompt: Context):
		self.prompt = prompt
	def set_contexts_cache(self, contexts_list: List[Context]):
		self._contexts_cache = contexts_list
	
	def unset_dirty(self):
		self._is_dirty = False
	def unset_prompt(self):
		self.prompt = None
	
	def add_context(self, context: SUPPORT_CONTEXT_TYPE):
		
		self.contexts.append(context)
		self.set_dirty()
		
	def _rebuild_contexts_cache_list(self) -> None:
		
		"""
		重建上下文缓存
		"""
		
		contexts_list = []
		
		for context in self.contexts:
			
			if isinstance(context, ContextsBlockProtocol):
				contexts_list.extend(ctx for ctx in context)
			else:
				contexts_list.append(context)
			
		# 最后把提示词插到第一个位置
		if self.prompt is not None:
			contexts_list.insert(0, self.prompt)
			
		self.set_contexts_cache(contexts_list)
		self.unset_dirty()
		
		return None
	
	def flatten_contexts(self) -> List[Context]:
		
		"""自动根据_is_dirty 重建/不重建"""
		
		if self.is_dirty():
			self._rebuild_contexts_cache_list()
		
		return self._contexts_cache