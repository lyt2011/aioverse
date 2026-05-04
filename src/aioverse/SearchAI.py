# 异步联网搜索AI客户端
from tavily import AsyncTavilyClient
# 密钥基类
from aioverse.models.errors import RunOutOfKeysError
# 密钥管理器协议
from aioverse.models.protocols import KeyManagerProtocol, LogProtocol


class TavilyClient:
	
	def __init__(
		self,
		keyManager	: KeyManagerProtocol,
		asyncLog	: LogProtocol
	):
		
		self.keyManager = keyManager
		
		# 日志实例注入
		self.asyncLog	= asyncLog
		
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
			"include_answer" : False,
			"include_images" : False,
			"max_results"    : 10,
			"timeout"        : 15
		}
		options.update(kwargs)
		
		await self.asyncLog.log(f"联网搜索参数 {options}", "debug")
		
		# 获取key
		key = self.keyManager.getAvailableKey()
		
		await self.asyncLog.log(f"开始联网搜索 {query}", "debug")
		
		_response = await (
			AsyncTavilyClient(api_key=key)
			.search(**options)
		)
		
		# response = _response.get("answer", "Error")
		response = _response.get("results", "Error")
		
		await self.asyncLog.log(f"联网搜索 {query} 结果: {response}", "debug")
		
		return response
