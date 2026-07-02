# 类型两件套
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Literal, Optional

from aioverse.base_models.segments		import Segment
from aioverse.base_models.tool_calling	import ToolCalling


class Context(BaseModel):
	
	model_config = ConfigDict(slots=True)
	
	role	: str
	content	: str | List[Segment]
	
	# 这个不一定会有
	reasoning_content: Optional[str] = None
	
	token: int = Field(exclude=True, default=0)
	
	def set_token(self, token: int): self.token = token

class User(Context):
	
	role: Literal["user"] = "user"

class Prompt(Context):
	
	role: Literal["system"] = "system"

class ToolCallingContext(Context):

	role		: Literal["assistant"] = "assistant"
	content		: str | List[Segment] | None = None
	
	# 新增tool_calls
	tool_calls	: List[ToolCalling]

class ToolOutput(Context):
	
	role		: Literal["tool"] = "tool"
	
	# 新增tool_call_id
	tool_call_id: str