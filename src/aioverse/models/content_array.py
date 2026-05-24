# 类型验证 类型注解
from pydantic import BaseModel, ConfigDict
from typing import List, Dict

# 上下文正文
from aioverse.types.content import Content


# 上下文正文数组
class ContentArray(BaseModel):
	
	model_config = ConfigDict(arbitrary_types_allowed=True)
	
	contents: List[Content]
	
	# 实现to_list方法
	def to_list(self) -> List[Dict[str, str]]:
		
		return [
			content.to_dict()
			for content in self.contents
		]