# 类型两件套
from pydantic import BaseModel, model_validator
from typing import List, Dict, Optional

from aioverse.base_models.contexts import Context, ToolCallingContext


class Choice(BaseModel):
	
	finish_reason		: str
	index				: int
	message				: Context | ToolCallingContext
	
class Usage(BaseModel):
	
	completion_tokens			: int
	prompt_tokens				: int
	total_tokens				: int
	completion_tokens_details	: Optional[Dict[str, int]] = None
	prompt_tokens_details		: Optional[Dict[str, int]] = None

class Response(BaseModel):
	
	id		: str
	choices	: List[Choice]
	created	: int
	model	: str
	object	: str
	usage	: Optional[Usage] = None