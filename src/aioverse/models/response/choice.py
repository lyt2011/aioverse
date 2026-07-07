from pydantic	import BaseModel, Field

from ..contexts	import Context, ToolCallingContext


class Choice(BaseModel):
	
	finish_reason		: str
	index				: int
	message				: Context | ToolCallingContext