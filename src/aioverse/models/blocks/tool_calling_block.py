from aioverse.protocols		import ContextsBlockProtocol
from ..contexts				import ToolOutput, Context, ToolCallingContext
from ..tool_calling			import ToolCalling

from pydantic	import Field, PrivateAttr
from typing		import List, Iterator


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
			self._tool_calling_ids = [tool_call.id for tool_call in self.tool_calling.tool_calls]
		
		return self._tool_calling_ids
	
	def verify_tool_ids(self) -> bool:
		
		"""验证tool_calling结果是否完整"""
		
		tool_output_ids = [tool_output.tool_call_id for tool_output in self.tool_outputs]
		
		return all((tool_calling_id in tool_output_ids) for tool_calling_id in self.tool_calling_ids)
	
	def delete(self, index: int): raise RuntimeError("ToolCallingBlock不支持该方法")
	def insert(self, index: int, context: ToolOutput): self.tool_outputs.insert(index, context)
	def append(self, context: ToolOutput): self.tool_outputs.append(context)