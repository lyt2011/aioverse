from typing import Optional, Dict, Any
from abc import ABC, abstractmethod 


class OpenAIProtocol(ABC):
	
	"""
	openai客户端协议
	"""
	
	# 必须实现的chatCompletion方法
	@abstractmethod
	async def chatCompletion(
		self,
		headers	: Optional[Dict[str, Any]]	= None,
		params	: Optional[Dict[str, Any]]	= None,
		body	: Optional[Dict[str, Any]]	= None,
		timeout	: int						= 90
	) -> str | Dict[str, Any]:
		
		"""
		异步创建聊天
		
		args:
			headers 请求头
			payload 请求参数
			params
			timeout 超时时间 默认90
		task:
			请求API并正确处理错误
		results:
			AI响应(字符串或者字典)
		"""
		
		pass