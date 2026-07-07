from pydantic	import BaseModel

from .function	import Function


class ToolCalling(BaseModel):

	id		: str
	type	: str
	function: Function