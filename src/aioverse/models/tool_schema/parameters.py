from pydantic	import BaseModel
from typing		import Dict, List

from .argument	import Argument


class Parameters(BaseModel):
	
	# 类型一般是object 不过不限 你爱填什么填什么
	type		: str = "object"
	properties	: Dict[str, Argument]
	required	: List[str]