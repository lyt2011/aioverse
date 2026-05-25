# 异步网络
import aiohttp
# 从包导入日志
from aioverse.Log import AsyncLog, AsyncWriter, LogFormatter
# 导入错误
from aioverse.errors import *
# 导入协议
from aioverse.protocols import LogProtocol
# 异步占位函数
from aioverse.utils.holder import NullObject
# 上下文 密钥管理器
from aioverse.managers import ContextManager, KeyManager
# 数据模型
from aioverse.models import ModelConfig

# 类型注解
from typing import Dict, List, Tuple, Any, Optional


class OpenAIClient:
	
	def __init__(
		self,
		model_config: ModelConfig,
		session		: aiohttp.ClientSession,
		async_log	: Optional[LogProtocol]	= None
	):
		
		self.model_config	= model_config
		self.key_manager	= KeyManager(model_config.model_keys)
		
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
		
		self.key_manager = key_manager
	
		return None
	
	async def call(
		self,
		context_manager	: ContextManager		,
		headers			: Dict[str, Any]	= {},
		params			: Dict[str, Any]	= {},
		body			: Dict[str, Any]	= {},
		timeout			: int				= 90,
	) -> Dict[str, Any]:
		
		# 构建请求参数 优先保证用户输入有效性
		params	= {**params}
		headers	= {
			"Authorization"	: self.key_manager.get_available_key(),
			"Content-Type"	: "application/json",
			**headers
		}
		body	= {
			"model"			: self.model_config.model_name,
			"messages"		: context_manager.to_list(),
			**body
		}
		
		await self.async_log.log("参数初始化完成 开始请求AI", "info")
		
		# 开始请求
		async with self.session.post(
			url		= self.model_config.api_url	,
			headers	= headers					,
			params	= params					,
			json	= body						,
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
		
		return response_json