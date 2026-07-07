from pydantic	import BaseModel, model_serializer
from typing		import Any, List, Union


_Empty = object()


class Argument(BaseModel):

	type		: Union[str, List[str]]
	description	: str
	default		: Any = _Empty
	
	@model_serializer(mode='wrap')
	def serialize(self, handler):
		
		data = handler(self)  # 先走默认序列化
		
		if self.default is not _Empty: data["default"] = self.default
		else: data.pop("default", None)
		
		return data