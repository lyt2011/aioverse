"""
定义AITools
ai可被调用的工具
"""

# 类型注解
from typing import Callable, Any, List, Tuple, Dict
# 专门用于ai使用的类型注解
from aioverse import Typing
# 函数工具
from functools import partial
# 获取时间实现
from datetime import datetime
# 重定向输出缓冲区
from contextlib import redirect_stdout
# 获取函数信息的一个模块
import inspect
# 异步实现
import asyncio
# io 顾名思义
import io

"""====================库导入===================="""

toolsListType = List[Tuple[Callable[Any, Any], Dict[str, Any]]]

"""====================类型定义==================="""

# ai可用的工具
class AITools:
	
	"""
	注意
	不要在函数定义的时候使用typing的类型注解
	非常不方便于解析
	
	如果必须使用嵌套的typing类型注解
	请使用aioverse.Typing
	"""
	
	# 搜索函数
	_searchFunc: Callable[str, str] = None
	
	@staticmethod
	async def searchOnline(query: Typing.String) -> str:
		
		"""
		联网搜索一个问题 并自动整合搜索结果
		
		args:
			query: 需要搜索的问题 str
		results:
			搜索结果: str
		"""
		
		# 联网搜索函数不为None时 获取联网搜索结果 否则结果就是""
		searchOnlineResult = await __class__._searchFunc(
			query = query
		) if __class__._searchFunc else ""
		
		return f"联网搜索结果: {searchOnlineResult}"
	
	@staticmethod
	def getBeijingTime() -> str:
		
		"""
		获取当前北京时间
		
		底层通过datetime库实现
		封装为字符串str返回
		"""
		
		return f"当前北京时间: {datetime.now()}"
	
	@staticmethod
	def add(a: Typing.Int, b: Typing.Int) -> str:
		
		"""
		计算两数只和
		
		args:
			a: 第一个加数 int
			b: 第二个加数 int
		results:
			string类型的 a + b 结果 str
		"""
		
		return f"{a}+{b} 的结果是: {a + b}"
	
	@staticmethod
	def syncExecuter(code: Typing.String) -> str:
		
		"""
		同步执行python代码
		
		args:
			code: 需要执行的代码 str
		results:
			代码执行结果 str
		"""
		
		# 创建字符串输出缓冲区
		stringBuffer = io.StringIO()
		
		# 重定向输出
		with redirect_stdout(stringBuffer):
			
			exec(code)
		
		# 判断缓冲区的值是否有内容
		if ( output := stringBuffer.getvalue() ):
			
			result = f"代码执行成功 结果: {output}"
		
		else:
			
			result = f"代码执行成功 没有结果"
		
		return result

"""====================类工具===================="""

def functionToDict(
	function: Callable[Any, Any]
) -> Dict[str, Any]:
	
	"""
	把函数转为dict
	"""
	
	# 函数的信息
	functionInfo				= {
		"name"			: "unknown",
		"description"	: "unknown",
		"params"		: {}
	}
	
	# 函数名
	functionInfo["name"]		= function.__name__
	# 函数文档(描述)
	functionInfo["description"]	= function.__doc__
	
	# 获取函数签名 并通过函数签名获取参数信息
	functionSignature			= inspect.signature(function)
	
	# 遍历函数参数信息 获取参数名/参数
	for paramName, param in functionSignature.parameters.items():
		
		# 参数类型
		paramType							= str(param.annotation)
		# 参数是否必须
		paramRequired						= param.default == inspect.Parameter.empty
		
		# 创建一个新的 paramName 键
		functionInfo["params"][paramName]	= {
			# 参数支持的类型
			"type"		: paramType,
			# 默认值 当参数必须时 填入"无默认值"
			# 当参数不是必须时 填入默认值 param.default
			"default"	: param.default if not paramRequired else "无默认值",
			# 该参数是否必须
			"required"	: paramRequired
		}
		
	return functionInfo

# 解析工具列表并从xx类中获取所需工具
def extractTools(
	classObj	: "AITools",
	tools		: List[ Dict[ str, Dict[ str, Any ] ] ]
) -> toolsListType:
	
	"""
	args:
		classObj 	: 任意一个拥有函数的容器
		tools 		: 装载工具的列表
	results:
		一个包含(函数 函数参数)的字典
	"""
	
	# 返回结果
	result = []
	
	# 获取所有工具
	for tool in tools:
		
		print(tool)
		
		# 获取函数名 函数参数
		toolName, toolParams = tool["name"], tool["params"]
		
		# 获取从classObj该函数
		toolObj = getattr(classObj, toolName, None)
		
		# 如果获取成功 则添加返回结果
		if toolObj: result.append(
			(
				toolObj,
				toolParams
			)
		)
	
	# 返回最终结果
	return result

# 获取一个类的所有可调用方法
def getClassFunction(
	classObject
) -> List[Tuple[str, Callable[Any, Any]]]:
	
	"""
	获取类的所有可调用方法
	返回方法对象
	"""
	
	return inspect.getmembers(
		classObject,
		predicate=inspect.isfunction
	)

# 工具执行器
async def toolExecuter(tools: toolsListType) -> List[Any]:
	
	"""
	解析所有工具并创建协程
	交给gather并发处理
	
	支持同步 异步函数
	
	args:
		工具列表
		详细请看toolsListType的定义
	"""
	
	# 创建协程对象列表
	cores = [
		function(**params) if asyncio.iscoroutinefunction(function)
		# 注意 这里不用lambda是因为 **params可能会被替换为最后一个参数
		else asyncio.to_thread( partial(function, **params) )
		for function, params in tools
	]
	
	# 直接并发
	results = await asyncio.gather(
		*cores,
		return_exceptions=True # 错误会当做字符串返回
	)
	
	# 返回处理结果
	return results

"""====================函数工具==================="""

if __name__ == "__main__":
	
	print(functionToDict(AITools.getBeijingTime))
	print(functionToDict(AITools.searchOnline))