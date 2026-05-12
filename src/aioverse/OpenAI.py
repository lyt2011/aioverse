# 异步网络
import aiohttp
# 从包导入日志
from aioverse.Log import AsyncLog, AsyncWriter, LogFormatter
# 导入错误
from aioverse.errors import *
# 导入协议
from aioverse.protocols import OpenAIProtocol, LogProtocol
# 导入数据体
from aioverse.types import Error, Item
# 异步占位函数
from aioverse.PlaceHolder import NullObject
# 上下文 密钥管理器
from aioverse.managers import ContextManager, KeyManager
# 从包导入错误处理常量
from aioverse.const import ExceptionHandlerAction
# json解析器
from aioverse.JsonParser import deepJsonParser
# 类型注解
from typing import Dict, List, Tuple, Any, Optional


# 全局会话
_globalSession = None

# 创建会话
def createSession() -> None:
	
	global _globalSession
	
	_globalSession = aiohttp.ClientSession()
	
	return None

# 获取会话
def getSession() -> aiohttp.ClientSession:
	
	global _globalSession
	
	return _globalSession

# 同步关闭
def syncCloseSession() -> None:
	
	"""
	注意这个不确保能运行
	"""
	
	asyncio.run(_globalSession.close())
	
	return None

# 异步关闭
async def asyncCloseSession() -> None:
	
	await _globalSession.close()
	
	return None


class OpenAIClient(OpenAIProtocol):
	
	"""
	Q: 为什么我要把__init__的context_manager弄去chatCompletion？
	A:srrqq
		因为原本我的设计理念是，一个client维护一个上下文
		然后我发现 这不太行 切换上下文很麻烦
		所以干脆让__init__管理密钥 对话时单独传入上下文
	"""
	
	def __init__(
		self,
		model		: str,
		api_url		: str,
		asyncLog	: Optional[LogProtocol]				= None,
		keyManager	: Optional[KeyManager]				= None,
		session		: Optional[aiohttp.ClientSession]	= None
	):
		
		"""
		args:
			model			: 模型名
			api_url			: api请求网址
			keyManager		: 密钥管理器
			context_manager	: 上下文管理器
		"""
		
		self.model		= model
		self.api_url	= api_url
		self.keyManager	= keyManager
		
		# 日志实例注入
		self.asyncLog	= asyncLog or NullObject()
		
		# 会话
		self.session	= session if session else getSession()
		
	def setKeyManager(
		self,
		keyManager: KeyManager
	) -> None:
		
		"""
		设置密钥管理器
		"""
		
		self.keyManager = keyManager
	
		return None
	
	async def chatCompletion(
		self,
		context_manager	: ContextManager		,
		headers			: Dict[str, Any]	= {},
		params			: Dict[str, Any]	= {},
		body			: Dict[str, Any]	= {},
		timeout			: int				= 90,
	) -> Item:
		
		"""
		args:
			params			: 请求参数
			headers			: 请求头
			body			: 请求体
			context_manager	: 上下文管理器
			timeout			: 超时时间
		task:
			构建所有参数
			并请求ai
			自动获取回复
		raise:
			ResponseCodeError: 返回码非200时
		results:
			ai回复
		"""
		
		# 构建请求参数 优先保证用户输入有效性
		params	= {
			**params
		}
		headers	= {
			"Authorization"	: self.keyManager.getAvailableKey(),
			"Content-Type"	: "application/json",
			**headers
		}
		body	= {
			"model"			: self.model,
			"messages"		: context_manager.toList(),
			**body
		}
		
		await self.asyncLog.log("参数初始化完成 开始请求AI", "info")
		# 开始请求
		async with self.session.post(
			url		= self.api_url	,
			headers	= headers		,
			params	= params		,
			json	= body			,
			timeout = timeout
		) as request:
			
			# 获取请求码
			requestCode = request.status
			# 获取请求返回
			rawResponse = deepJsonParser(await request.text())
		
		await self.asyncLog.log(f"请求完成: {requestCode}", "info")
		
		# 防止api返回出错
		if not isinstance(rawResponse, dict): raise RuntimeError(rawResponse)
		
		# 返回码不为200
		if requestCode != 200:
			
			# 抛出报错 带上返回/请求码
			raise ResponseCodeError(
				code		= requestCode,
				response	= rawResponse
			)
		
		# 获取具体信息
		message = rawResponse.get("choices", [{}])[0].get("message", {})
		# 获取token用量
		usage	= rawResponse.get("usage")
		
		# 请求数据
		data	= Item(
			model		= rawResponse.get("model"),
			request_id	= rawResponse.get("id"),
			content		= message.get("content"),
			reasoning	= message.get("reasoning_content"),
			token		= Item(
				prompt		= usage.get("prompt_tokens"),
				completion	= usage.get("completion_tokens"),
				total		= usage.get("total_tokens"),
				cached		= usage.get("cached_tokens")
			))
		
		await self.asyncLog.log("返回数据构建成功", "debug")
		
		return data