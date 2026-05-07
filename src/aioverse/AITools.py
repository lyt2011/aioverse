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