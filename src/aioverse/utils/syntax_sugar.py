from aioverse.managers					import ContextManager
from aioverse.base_models.contexts		import Context
from aioverse.base_models.segments		import Segment
from aioverse.base_models.tool_schema	import Tool, Function, Parameters , Argument, _Empty

from typing import List, Dict, Any, Tuple


# 快速构建工具schema
def build_tool_schema(
	tool_name		: str,
	tool_description: str,
	requirements	: List[str],
	arguments		: Dict[str, Tuple[str, str]]
) -> Tool:
	
	"""
	理想的requirements:
		[<arg1>, <arg2>, ...]
	理想的arguments:
		{<name>: (<type>, <description>, <Optional<default>>)}
	"""
	
	# 校验格式
	# 校验arguments格式是否正确
	args_is_right	= all(
		isinstance(arg, tuple) and len(arg) >= 2
		for name, arg in arguments.items()
	)
	# 校验必须参数是否存在于所有参数里
	reqs_is_right	= all(name in arguments for name in requirements)
	
	if not (reqs_is_right and args_is_right): raise ValueError("错误的参数格式")
	
	# 构建所有Argument
	args		= {
		name: Argument(
			type		= arg[0],
			description	= arg[1],
			default		= arg[2] if len(arg) == 3 else _Empty
		)
		for name, arg in arguments.items()
	}
	# 构建Parameters
	params		= Parameters(
		properties	= args,
		required	= requirements
	)
	# 构建Function
	function	= Function(
		name		= tool_name,
		description	= tool_description,
		parameters	= params
	)
	
	# 返回已构建完成的Tool
	return Tool(function=function)

def build_tool_schema_by_doc(func: callable) -> Tool:
	
	"""
	野路子
	
	写着写着想到个好玩的 通过在函数注释写json
	通过该方法解析后透传给build_tool_schema
	然后实现动态工具schema🤓🤓🤓
	但是目前别用这个
	感觉确实有点野
	"""
	
	return build_tool_schema(**orjson.loads(func.__doc__))