from pydantic	import Field
from typing		import List, Iterator

from ..contexts		import Context
from ...protocols	import ContextsBlockProtocol


class ContextsBlock(ContextsBlockProtocol):
	
	contexts: List[Context] = Field(default_factory=list)
	
	def __len__(self) -> int: return len(self.contexts)
	def __iter__(self) -> Iterator[Context]: yield from self.contexts
	
	def delete(self, index: int): self.contexts.pop(index)
	def insert(self, index: int, context: Context): self.contexts.insert(index, context)
	def append(self, context: Context): self.contexts.append(context)