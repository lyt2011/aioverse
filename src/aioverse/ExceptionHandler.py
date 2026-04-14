"""====================库导入===================="""
# 类型注解
from typing import Callable, Union, Any, Dict
# 错误协议
from aioverse.models.protocols import ExceptionHandlerProtocol
# 导入错误
from aioverse.models.errors import ResponseCodeError

"""==================定义返回类型==================="""

CONTINUE	= "continue"
ABORT		= "abort"
RETRY		= "retry"

"""===================处理器定义===================="""
# 专门处理api请求的类
class ApiRequestExceptionHandler(ExceptionHandlerProtocol):
	
	def __init__(self):
		
		# 错误码对应处理器
		self.code2handler = {
			
			"429": self._TMQHandler
			
		}
	
	def __call__(
		self,
		error: ResponseCodeError
	) -> str | None:
		
		# 获取错误码/api请求结果
		code		= str( getattr(error, "code", None) )
		response	= getattr(error, "response", None)
		
		# 获取对应处理函数
		handler		= self.code2handler.get(code)
		
		# 判断是否未定义
		if not handler: return None
		
		# 否则返回处理结果
		return handler(
			code		= code,
			response	= response
		)
	
	# 设置处理器
	def setHandler(
		self			,
		code	: str	,
		handler	: Callable
	) -> None:
		
		self.code2handler[code] = handler
		
		return None
	
	# 删除处理器
	def deleteHandler(
		self		,
		code: str
	) -> None:
		
		# 判断是否不存在该错误
		if code not in self.code2handler:
			
			return None
		
		# 存在就调用del删除
		del self.code2handler[code]
		
		return None
	
	# 处理402(太多请求)
	def _TMQHandler(
		self					,
		code	: str			,
		response: Dict[str, Any]
	) -> str:
		
		# 获取原数据
		metadata = (
			response
			.get("error", {})
			.get("metadata")
		)
		
		# 判断是否错误的元数据
		if (
			not metadata or
			not isinstance(metadata, dict)
		):
						
			raise RuntimeError(f"未知的错误: {response}")
			
		# 返回
		return (
			# headers存在 密钥用完
			ABORT if "headers" in metadata
			# 否则就是请求过多
			else RETRY
		)