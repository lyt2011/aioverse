from pydantic	import BaseModel, ConfigDict, Field
from typing		import List, Optional

from ..segments	import Segment


class Context(BaseModel):
	
	model_config = ConfigDict(slots=True)
	
	role				: str
	content				: str | List[Segment]
	reasoning_content	: Optional[str] = None
	
	token: int = Field(exclude=True, default=0)
	
	def set_token(self, token: int): self.token = token