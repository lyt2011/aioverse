from abc		import ABC, abstractmethod
from typing		import Optional, List, Iterator
from pydantic	import BaseModel

from aioverse.base_models.contexts import Context


class ContextsBlockProtocol(ABC, BaseModel):
	
	@abstractmethod
	def __iter__(self) -> Iterator[Context]: ...
	
	@abstractmethod
	def __len__(self) -> int: ...
	
	@abstractmethod
	def delete(self, index: int): ...
	
	@abstractmethod
	def insert(self, index: int, context: Context): ...
	
	@abstractmethod
	def append(self, context: Context): ...