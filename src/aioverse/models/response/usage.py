from pydantic	import BaseModel, Field
from typing		import Dict


class Usage(BaseModel):
	
	completion_tokens			: int
	prompt_tokens				: int
	total_tokens				: int
	completion_tokens_details	: Dict[str, int] = Field(default_factory=dict)
	prompt_tokens_details		: Dict[str, int] = Field(default_factory=dict)
