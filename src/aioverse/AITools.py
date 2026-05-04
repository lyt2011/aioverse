"""
定义AITools
ai可被调用的工具
"""

# 类型注解
from typing import Callable, Any, List, Tuple, Dict, Optional
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
# 生成哈希
import uuid
# 异步文件读写
import aiofiles

"""====================库导入===================="""

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
	async def searchOnline(
		query: Typing.String
	) -> str:
		
		"""
		联网搜索一个问题，将结果写入文件后返回与文件对应的哈希值
		"""
		
		# 搜索具体内容
		searchOnlineResult	= await __class__._searchFunc(
			query = query
		) if __class__._searchFunc else "联网搜索已被禁用"
		
		# 随机生成一串哈希
		fileHash			= uuid.uuid4().hex
		
		# 哈希直接作为文件名写入/tmp
		async with aiofiles.open(
			f"/tmp/{fileHash}",
			"w",
			encoding="utf-8"
		) as file:
			
			await file.write(searchOnlineResult)
		
		# 返回这串哈希
		return f"{fileHash}"
	
	@staticmethod
	async def readFileByHash(
		hash: Typing.String
	) -> str:
		
		"""
		通过哈希值获取文件内容
		"""
		
		async with aiofiles.open(
			f"/tmp/{hash}",
			encoding="utf-8"
		) as file:
			
			fileContent = await file.read()
		
		return fileContent
	
	@staticmethod
	async def writeFileByHash(
		hash: Typing.String,
		path: Typing.String
	) -> str:
		
		"""
		通过hash值获取文件内容
		并写入到path指定的文件
		"""
		
		# 通过readFileByHash读取哈希文件内容
		fileContent = await __class__.readFileByHash(hash=hash)
		
		# 写入path
		async with aiofiles.open(
			path,
			"w",
			encoding="utf-8"
		) as file:
			
			await file.write(fileContent)
		
		return f"{path} 写入成功"
	
	@staticmethod
	def getBeijingTime() -> str:
		
		"""
		获取当前北京时间
		"""
		
		return f"当前北京时间: {datetime.now()}"
	
	@staticmethod
	def add(a: Typing.Int, b: Typing.Int) -> str:
		
		"""
		计算两数只和
		"""
		
		return f"{a}+{b} 的结果是: {a + b}"
	
	@staticmethod
	def syncExecuter(code: Typing.String) -> str:
		
		"""
		同步执行python代码
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

# 函数工具
class FunctionTools:
	
	# 函数参数转字典
	@staticmethod
	def functionParamToDict(
		function: Callable[Any, Any]
	) -> Dict[str, Any]:
		
		"""
		函数参数转Dict
		"""
		
		# 参数
		params = {}
		
		# 提取参数名与参数信息
		paramInformation	= inspect.signature(function).parameters.items()
		
		# 遍历所有参数 获取信息
		for name, param in paramInformation:
			
			# 参数类型
			paramType		= str(param.annotation)
			# 参数是否必须
			is_required		= param.default == inspect.Parameter.empty
			
			params[name]	= {
				"type"		: str(param.annotation),
				"default"	: None if is_required else param.default,
				"required"	: is_required
			}
		
		return params
	
	# 函数转字典
	@staticmethod
	def functionToDict(
		function: Callable[Any, Any]
	) -> Dict[str, Any]:
		
		data = {
			"name"			: function.__name__,
			"description"	: function.__doc__,
			"params"		: __class__.functionParamToDict(function)
		}
		
		return data

# 获取一个实例的所有可调用方法
def getFunctionFromObject(
	instance: type
) -> List[Tuple[str, Callable[Any, Any]]]:
	
	"""
	获取类的所有可调用方法
	返回方法对象
	"""
	
	return inspect.getmembers(
		instance,
		predicate=inspect.isfunction
	)

# 工具执行器
async def toolExecuter(
	tools	: List[Dict[str, Dict[str, Any]]],
	obj		: Optional[type] = None
) -> List[Any]:
	
	"""
	解析所有工具并创建协程
	交给gather并发处理
	
	支持同步 异步函数
	
	理想的tools参数:
	[
		{
			"searchOnline": {
				"query": "蔡徐坤"
			}
		},
		{
			"add": {
				"a": 1,
				"b": 2
			}
		}
	]
	即一个列表的每一个元素都是一个工具信息
	工具信息即以工具名为键，参数字典为值的字典
	"""
	
	# 转换str为相应函数
	functionAndParams	= [
		(getattr(obj, name), params)
		for toolDict in tools
		for name, params in toolDict.items()
	]
	
	# 创建协程对象列表
	coros				= [
		function(**params) if asyncio.iscoroutinefunction(function)
		# 注意 这里不用lambda是因为 **params可能会被替换为最后一个参数
		else asyncio.to_thread(partial(function, **params))
		for function, params in functionAndParams
	]
	
	# 直接并发
	results = await asyncio.gather(
		*coros,
		return_exceptions=True # 错误会返回
	)
	
	# 返回处理结果
	return results

"""====================函数工具==================="""

if __name__ == "__main__":
	
	tools	= {
		name: FunctionTools.functionToDict(function)
		for name, function in getFunctionFromClass(AITools)
	}
	
	print(tools)