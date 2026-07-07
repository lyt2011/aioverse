from .base_context	import Context

from typing	import Literal


class ToolOutput(Context):
	
	role		: Literal["tool"] = "tool"
	tool_call_id: str