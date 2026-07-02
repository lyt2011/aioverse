from aioverse.Log				import AsyncLog, AsyncWriter, LogFormatter
from aioverse.errors			import *
from aioverse.protocols			import LogProtocol
from aioverse.utils.holder		import NullObject
from aioverse.managers			import ContextManager
from aioverse.base_models		import ModelConfig, AssistantKey
from aioverse.models.response	import Response

# 类型注解
from typing import Dict, List, Tuple, Any, Optional

import aiohttp


class OpenAIClient:
	
	def __init__(
		self,
		model_config: ModelConfig,
		session		: aiohttp.ClientSession,
		async_log	: Optional[LogProtocol]	= None
	):
		
		self.model_config	= model_config
		self.session		= session
		
		self.async_log = async_log or NullObject()
	
	async def call(
		self,
		context_manager	: ContextManager		,
		assistant_key	: AssistantKey			,
		headers			: Dict[str, Any]	= {},
		params			: Dict[str, Any]	= {},
		body			: Dict[str, Any]	= {},
		timeout			: int				= 90,
	) -> Response:
		
		# 构建请求参数 优先保证用户输入有效性
		params	= {**params}
		headers	= {
			"Authorization"	: assistant_key.key,
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
		
		return Response.model_validate(response_json)