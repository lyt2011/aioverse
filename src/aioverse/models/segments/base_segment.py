from pydantic	import BaseModel
from typing		import Dict

import orjson


class Segment(BaseModel):
	
	type: str
	data: str
	
	def model_dump(self) -> Dict[str, str]:
		
		return {"type": self.type, self.type: self.data}
	
	def model_dump_json(self) -> str:
		
		return orjson.dumps(self.model_dump()).decode()