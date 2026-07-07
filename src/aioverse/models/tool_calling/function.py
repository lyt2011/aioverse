from pydantic	import BaseModel


class Function(BaseModel):
	
	name		: str
	arguments	: str # Json
