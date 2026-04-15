# 异步网络
import aiohttp
# 从包导入日志
from aioverse.Log import AsyncLog, AsyncWriter, LogFormatter
# 导入错误
from aioverse.models.errors import *
# 导入协议
from aioverse.models.protocols import OpenAIProtocol, ContextManagerProtocol, KeyManagerProtocol, ExceptionHandlerProtocol
# 导入数据体
from aioverse.models.structs import Error
# 从包导入错误处理常量
from aioverse.const import ExceptionHandlerAction
# 类型注解
from typing import Dict, List, Tuple, Any, Optional

"""====================库导入===================="""

class ChatBuilder:
	
	"""构建对话字典"""
	
	@staticmethod
	def user(content: str) -> Dict[str, str]:
		
		data = {
			"role"		: "user",
			"content"	: content
		}
		
		return data
	
	@staticmethod
	def ai(content: str) -> Dict[str, str]:
		
		data = {
			"role"		: "assistant",
			"content"	: content
		}
		
		return data
	
	@staticmethod
	def system(content: str) -> Dict[str, str]:
		
		data = {
			"role"		: "system",
			"content"	: content
		}
		
		return data
	
	@staticmethod
	def tool(content: dict) -> Dict[str, Dict[str, Any]]:
		
		data = {
			"role"		: "tool",
			"content"	: content
		}
		
		return data

"""====================封装对话==================="""

class OpenAIClient(OpenAIProtocol):
	
	"""
	Q: 为什么我要把__init__的contextManager弄去chatCompletion？
	A:
		因为原本我的设计理念是，一个client维护一个上下文
		然后我发现 这不太行 切换上下文很麻烦
		所以干脆让__init__管理密钥 对话时单独传入上下文
	"""
	
	def __init__(
		self,
		model			: str,
		apiUrl			: str,
		keyManager		: Optional[KeyManagerProtocol]	= None
	):
		
		"""
		args:
			model			: 模型名
			apiUrl			: api请求网址
			keyManager		: 密钥管理器
			contextManager	: 上下文管理器
		"""
		
		self.model				= model
		self.apiUrl				= apiUrl
		self.keyManager			= keyManager
		
	def setKeyManager(
		self,
		keyManager: KeyManagerProtocol
	) -> None:
		
		"""
		设置密钥管理器
		"""
		
		self.keyManager = keyManager
		
		return None
	
	# 从密钥管理器中获取key
	def getKey(self) -> str:
		
		"""
		从密钥管理器获取key
		"""
		
		# 判断密钥管理器是否未初始化
		if not self.keyManager:
			
			raise RuntimeError("密钥管理器未初始化")
		
		key = (
			# 获取当前key 赋值给key
			self.keyManager.getCurrentKey()
			# 如果获取的是空 则获取下一个key
			or self.keyManager.getNextKey()
		)
		
		return key
	
	async def chatCompletion(
		self,
		headers			: Optional[Dict[str, Any]]			= None	,
		params			: Optional[Dict[str, Any]]			= None	,
		body			: Optional[Dict[str, Any]]			= None	,
		contextManager	: Optional[ContextManagerProtocol]	= None
		timeout			: int								= 90	,
		returnRaw		: bool								= False
	) -> str:
		
		"""
		args:
			params			: 请求参数
			headers			: 请求头
			body			: 请求体
			contextManager	: 上下文管理器
			timeout			: 超时时间
			returnRaw		: 返回原始信息
		task:
			构建所有参数
			并请求ai
			自动获取回复
		raise:
			ResponseCodeError: 返回码非200时
		results:
			ai回复
		"""
		
		# 获取key
		key				= self.getKey()
		
		# 构建请求参数 标准api是不需要参数的
		defaultParams	= {}
		# 构建请求头
		defaultHeaders	= {
			"Authorization"	: key,
			"Content-Type"	: "application/json"
		}
		# 构建请求体 (不同api之间可使用的参数不一样)
		defaultBody		= {
			"model"			: self.model,
			"messages"		: contextManager.toList()
		}
		
		# 优先保证用户输入有效性
		if headers	: defaultHeaders.update(headers)
		if params	: defaultParams	.update(params)
		if body		: defaultBody	.update(body)
		
		# 开始请求
		async with aiohttp.ClientSession() as session:
			async with session.post(
				url		= self.apiUrl	,
				headers	= defaultHeaders,
				params	= defaultParams	,
				json	= defaultBody	,
				timeout = timeout
			) as request:
				
				# 获取请求码
				requestCode = request.status
				# 获取请求返回
				rawResponse = await request.json()
		
		# 返回码不为200
		if requestCode != 200:
			
			# 抛出报错 带上返回/请求码
			raise ResponseCodeError(
				code		= requestCode,
				response	= rawResponse
			)
		
		# 尝试获取具体回复
		response = (
			rawResponse
			.get( "choices", [ {} ] )[0] # 默认返回{} 保证下层get正常调用
			.get( "message", {} )
			.get( "content", "Error")
		) if not returnRaw else rawResponse
		
		return response

"""==================对OpenAI的高级封装================="""

# 安全的请求
async def safeRequest(
	openAIClient		: OpenAIProtocol,
	exceptionHandler	: ExceptionHandlerProtocol,
	maxRetryCount		: int = 3,
	**kwargs
) -> Error | str:
	
	"""
	一个安全的ai请求接口
	
	args:
		openAIClient		: openai客户端 OpenAIProtocol协议
		exceptionHandler	: 错误处理器 ExceptionHandlerProtocol协议
		maxRetryCount		: 最大重试次数 int 默认3
		retryCount			: 已重试次数 int 默认0
		**kwargs			: 用于装载请求参数 dict
	results:
		Error类型 / str
	"""
	
	# 获取已重试的次数
	_retryCount = kwargs.get("_retryCount", 0)
	
	try:
		
		response = await openAIClient.chatCompletion(**kwargs)
	
	except ResponseCodeError as error:
		
		# 处理这个错误
		# (这里不处理内部的typeerror错误是因为我通过except获取的错误不可能会错)
		handleResult = exceptionHandler(error)
		
		# 解析处理结果
		# 重试？
		if handleResult == ExceptionHandlerAction.RETRY:
			
			# 判断是否超过最大重试次数
			if _retryCount > maxRetryCount:
				
				# 直接返回
				return Error(
					code		= error.code,
					message		= f"超过最大重试次数限制 {maxRetryCount}",
					metaData	= error.response
				)
			
			# 递归函数 重试
			return safeRequest(
				openAIClient		= openAIClient,
				exceptionHandler	= exceptionHandler,
				maxRetryCount		= maxRetryCount,
				**kwargs,
				_retryCount			= _retryCount + 1 # _retry在下面是因为**kwargs包含了_retry 这样可以防止变量被替换
			)
		
		# 终止？
		if handleResult == ExceptionHandlerAction.ABORT:
			
			# 直接返回
			return Error(
				code		= error.code,
				message		= f"主动终止了请求",
				metaData	= error.response
			)
		
		# 都不是 一般不会
		return Error(
			code 		= error.code,
			message		= "未知的处理结果",
			metaData	= error.response
		)
	
	# 其他错误暂时不处理
	except Exception as error: raise
	
	# 没错就返回结果
	return response

"""========================函数定义====================="""

