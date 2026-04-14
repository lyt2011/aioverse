# 异步联网搜索AI客户端
from tavily import AsyncTavilyClient
# 密钥基类
from aioverse.models.errors import RunOutOfKeysError
# 密钥管理器协议
from aioverse.models.protocols import KeyManagerProtocol
# 日志
from .Log import AsyncLog, AsyncWriter, LogFormatter


class TavilyClient:
	
	def __init__(
		self,
		keyManager: KeyManagerProtocol
	):
		
		self.keyManager = keyManager
		
	async def search(
		self,
		query: str,
		**kwargs
	) -> str:
		
		"""
		联网搜索一个问题
		"""
		
		options = {
			"query"          : query,
			"include_answer" : True,
			"include_images" : False,
			"max_results"    : 20,
			"timeout"        : 15
		}
		options.update(kwargs)
		
		# await Log.log(f"传入参数为 {options} 问题: {query}", "Debug")
		
		# 获取key
		if not (key := self.keyManager.getCurrentKey()):
			
			if not (key := self.keyManager.getNextKey()):
				
				raise RunOutOfKeysError
		
		# await Log.log(f"开始联网搜索 {query}", "info")
		
		_response = await (
			AsyncTavilyClient(api_key=key)
			.search(**options)
		)
		
		response = _response.get("answer", "Error")
		
		# await Log.log(f"联网搜索 {query} 完成: {response}", "info")
		
		return response
