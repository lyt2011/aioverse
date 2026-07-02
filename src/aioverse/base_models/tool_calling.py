# 类型两件套
from pydantic import BaseModel


class Function(BaseModel):
	
	name		: str
	arguments	: str # 其实是Json

# 单个工具请求
class ToolCalling(BaseModel):

	id		: str
	type	: str
	function: Function