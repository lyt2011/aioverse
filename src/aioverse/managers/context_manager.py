from typing import List, Dict, Optional, Any

from aioverse.base_models.contexts				import Prompt, Context, ToolOutput, ToolCallingContext
from aioverse.models.blocks						import ToolCallingBlock, ContextsBlock
from aioverse.models							import _ContextsStatus
from aioverse.protocols.contexts_block_protocol	import ContextsBlockProtocol


class ContextManager:
	
	__slots__ = ["contexts_status"]
	
	def __init__(
		self,
		contexts_status: _ContextsStatus | None = None
	):
		
		self.contexts_status = contexts_status or _ContextsStatus()
	
	@property
	def token(self) -> int:
		
		return self.contexts_status.token
	
	def set_token(self, token: int):
	
		self.contexts_status.token = token
		
		return None
	
	def set_prompt(self, prompt: Context):
		
		self.contexts_status.prompt = prompt
		
		return None
	
	def has_prompt(self) -> bool:
		
		return bool(self.contexts_status.prompt)
	
	def get_prompt(self) -> Context | None:
		
		return self.contexts_status.prompt
	
	def add_context(self, context: Context | ContextsBlockProtocol):
		
		self.contexts_status.contexts.append(context)
		
		return None
	
	def to_list(self) -> List[Dict[str, Any]]:
	
		contexts_list = []
		
		for context in self.contexts_status.contexts:
			
			if isinstance(context, ContextsBlockProtocol):
				
				contexts_list.extend(ctx.model_dump() for ctx in context)
			
			else:
				
				contexts_list.append(context.model_dump())
		
		if self.contexts_status.prompt is not None:
			
			contexts_list.insert(0, self.contexts_status.prompt.model_dump())
		
		return contexts_list
	
	def trim(self):
	
		self.contexts_status.contexts.pop(0)
		
		return None
	
	def clear(self, keep_prompt: bool = True):
		
		self.contexts_status.contexts.clear()
		
		if not keep_prompt: self.contexts_status.prompt = None
		
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