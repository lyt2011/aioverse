# 类型两件套
from pydantic import Field, PrivateAttr
from typing import List, Iterator

from aioverse.base_models.contexts				import ToolOutput, Context, ToolCallingContext
from aioverse.base_models.tool_calling			import ToolCalling
from aioverse.protocols.contexts_block_protocol	import ContextsBlockProtocol


class ToolCallingBlock(ContextsBlockProtocol):
	
	"""
	工具调用块 (ToolCalling Block)
	包含请求与结果
	不支持delete方法: 破坏调用链结构👎🏻
	"""
	
	tool_calling	: ToolCallingContext
	tool_outputs	: List[ToolOutput] = Field(default_factory=list)
	
	# 懒加载 防止一直计算id
	_tool_calling_ids: List[str] = PrivateAttr(default=None)
	
	def __iter__(self) -> Iterator[Context]:
		
		yield self.tool_calling
		yield from self.tool_outputs
	
	def __len__(self) -> int:
	
		return len(self.tool_calling.tool_calls) + len(self.tool_outputs)
	
	@property
	def tool_calling_ids(self) -> List[str]:
		
		"""懒加载tool_calling_ids实现"""
		
		if self._tool_calling_ids is None:
		
			self._tool_calling_ids = [
				tool_call.id
				for tool_call in self.tool_calling.tool_calls
			]
		
		return self._tool_calling_ids
	
	def verify_tool_ids(self) -> bool:
		
		"""验证tool_calling结果是否完整"""
		
		# 获取tool_responses的所有id
		tool_response_ids	= [ter.tool_call_id for ter in self.tool_outputs]
		
		return all(
			tool_calling_id in tool_response_ids
			for tool_calling_id in self.tool_calling_ids
		)
	
	def delete(self, index: int): raise RuntimeError("ToolCallingBlock不支持该方法")
	def insert(self, index: int, context: ToolOutput): self.tool_outputs.insert(index, context)
	def append(self, context: ToolOutput): self.tool_outputs.append(context)

class ContextsBlock(ContextsBlockProtocol):
	
	contexts: List[Context] = Field(default_factory=list)
	
	def __len__(self) -> int: return len(self.contexts)
	def __iter__(self) -> Iterator[Context]: yield from self.contexts
	
	def delete(self, index: int): self.contexts.pop(index)
	def insert(self, index: int, context: Context): self.contexts.insert(index, context)
	def append(self, context: Context): self.contexts.append(context)