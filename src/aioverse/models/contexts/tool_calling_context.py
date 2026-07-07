from .base_context	import Context
from ..segments		import Segment
from ..tool_calling	import ToolCalling

from typing	import Literal, List


# TODO 这里不用自定义(S什么鬼的那个)会导致输入与输出不一样
class ToolCallingContext(Context):

	role		: Literal["assistant"] = "assistant"
	content		: str | List[Segment] | None = None
	
	# 新增tool_calls
	tool_calls	: List[ToolCalling]