# 异步网络
import aiohttp
# 从包导入日志
from aioverse.Log import AsyncLog, AsyncWriter, LogFormatter
# 导入错误
from aioverse.errors import *
# 导入协议
from aioverse.protocols import LogProtocol
# 导入数据体
from aioverse.types import Error, Item
# 异步占位函数
from aioverse.utils.holder import NullObject
# 上下文 密钥管理器
from aioverse.managers import ContextManager, KeyManager
# 类型注解
from typing import Dict, List, Tuple, Any, Optional


class OpenAIClient:
	
	def __init__(
		self,
		model		: str,
		api_url		: str,
		session		: aiohttp.ClientSession,
		async_log	: Optional[LogProtocol]	= None,
		key_manager	: Optional[KeyManager]	= None
	):
		
		"""
		args:
			model			: 模型名
			api_url			: api请求网址
			keyManager		: 密钥管理器
			context_manager	: 上下文管理器
		"""
		
		self.model			= model
		self.api_url		= api_url
		self.key_manager	= key_manager
		
		# 日志实例注入
		self.async_log	= async_log or NullObject()
		
		# 会话 尝试通过session获取
		self.session	= session
		
	def set_key_manager(
		self,
		key_manager: KeyManager
	) -> None:
		
		"""
		设置密钥管理器
		"""
		
		self.key_manager = keyManager
	
		return None
	
	async def call(
		self,
		context_manager	: ContextManager		,
		headers			: Dict[str, Any]	= {},
		params			: Dict[str, Any]	= {},
		body			: Dict[str, Any]	= {},
		timeout			: int				= 90,
	) -> Item:
		
		# 构建请求参数 优先保证用户输入有效性
		params	= {**params}
		headers	= {
			"Authorization"	: self.key_manager.get_available_key(),
			"Content-Type"	: "application/json",
			**headers
		}
		body	= {
			"model"			: self.model,
			"messages"		: context_manager.to_list(),
			**body
		}
		
		await self.async_log.log("参数初始化完成 开始请求AI", "info")
		
		# 开始请求
		async with self.session.post(
			url		= self.api_url	,
			headers	= headers		,
			params	= params		,
			json	= body			,
			timeout = timeout
		) as request:
			
			# 获取返回码
			response_code = request.status
			# 获取请求返回
			response_json = await request.json()
		
		await self.async_log.log(f"请求完成: {response_code}", "info")
		
		# 返回码不为200
		if response_code != 200:
			
			# 抛出报错 带上返回/请求码
			raise ResponseCodeError(
				code		= response_code,
				response	= response_json
			)
		
		# 获取具体信息
		message = response_json.get("choices", [{}])[0].get("message", {})
		# 获取token用量
		usage	= response_json.get("usage")
		
		# 请求数据
		data	= Item(
			model		= response_json.get("model"),
			request_id	= response_json.get("id"),
			content		= message.get("content"),
			reasoning	= message.get("reasoning_content"),
			token		= Item(
				prompt		= usage.get("prompt_tokens"),
				completion	= usage.get("completion_tokens"),
				total		= usage.get("total_tokens"),
				cached		= usage.get("cached_tokens")
			))
		
		await self.async_log.log("返回数据构建成功", "debug")
		
		return data