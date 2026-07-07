from typing import List, Dict, Optional, Any

from aioverse.models	import (
	Prompt,
	Context,
	ToolOutput,
	ToolCallingContext,
	ToolCallingBlock,
	ContextsBlock,
	_ContextsStatus,
	SUPPORT_CONTEXT_TYPE
)
from ..protocols	import ContextsBlockProtocol


class ContextManager:
	
	__slots__ = ["contexts_status"]
	
	def __init__(self, contexts_status: Optional[_ContextsStatus] = None):
		
		self.contexts_status = contexts_status or _ContextsStatus()
	
	@property
	def token(self) -> int:
		return self.contexts_status.token
	
	def set_token(self, token: int):
		self.contexts_status.set_token(token)
	def set_prompt(self, prompt: Context):
		self.contexts_status.set_prompt(prompt)
		
	def has_prompt(self) -> bool:
		return bool(self.contexts_status.prompt)
	
	def get_prompt(self) -> Context | None:
		return self.contexts_status.prompt
	
	def add_context(self, context: SUPPORT_CONTEXT_TYPE):
		self.contexts_status.add_context(context)
	
	def flatten_contexts(self) -> List[Context]:
		return self.contexts_status.flatten_contexts()
	def to_list(self) -> List[Dict[str, Any]]:
		return [ctx.model_dump() for ctx in self.flatten_contexts()]
	
	def trim(self):
		self.contexts_status.contexts.pop(0)
	
	def clear(self, keep_prompt: bool = True):
		
		self.contexts_status.contexts.clear()
		
		if keep_prompt is False:
			self.contexts_status.unset_prompt()
		
		return None
	
	def to_file(self, path: str, encoding: str = "utf-8"):
		
		"""
		设计理念: 默认同步 通过重写方法达到异步支持
		(正常情况下上下文持久化只需要在程序结束时执行)
		"""
		
		with open(path, "w", encoding=encoding) as file: file.write(self.contexts_status.model_dump_json())
		
		return None
	
	@classmethod
	def from_file(cls, path: str, encoding: str = "utf-8") -> "ContextManager":
		
		"""设计理念与to_file相同"""
		
		with open(path, encoding=encoding) as file:
			
			_context_status = _ContextsStatus.model_validate_json(file.read())
		
		return cls(_context_status)