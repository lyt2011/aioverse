from pydantic	import BaseModel, Field, SerializeAsAny
from typing		import List

from aioverse.base_models.contexts	import Context, Prompt
from aioverse.models.blocks			import ToolCallingBlock, ContextsBlock


class _ContextsStatus(BaseModel):
	
	"""上下文的内部状态 (提供给ContextManager使用)"""
	
	contexts: List[Context | ToolCallingBlock | ContextsBlock]	= Field(default_factory=list)
	prompt	: Context | Prompt | None							= Field(default=None)
	
	token	: int	= Field(default=0)