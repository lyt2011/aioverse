# 类型注解
from typing import List
# 抽象接口
from aioverse.models.protocols import KeyManagerProtocol


class KeyManager(KeyManagerProtocol):
	
	"""密钥管理"""
	
	def __init__(
		self,
		keysList: List[str]
	):
		
		# 防止出现None的情况 先对列表进行格式化
		self._keysList = [
			key
			for key in keysList
			if isinstance(key, str) # 仅允许字符串类型的密钥
		]
		
		# 当前引索/密钥
		self.usingKey  = (-1, None)
	
	def __str__(self) -> str:
		
		return "->".join(self._keysList)
		
	def __len__(self) -> int:
		
		return len(self._keysList)
	
	# 获取下一个密钥
	def getNextKey(self) -> str:
		
		"""
		获取下一个Key
		没有则抛出RuntimeError
		"""
		
		# 解包self.usingKey 获取当前引索/key
		currentIndex, usingKey	= self.usingKey
		nextIndex				= currentIndex + 1
		
		"""
		只需要判断是否需求数量少于引索即可
		列表里只有key了
		"""
		if len(self._keysList) - 1 < nextIndex: 
			
			raise RunOutOfKeysError("没有Key可继续使用")
		
		# 存在则获取该key
		nextKey					= self._keysList[nextIndex]
		# 更换self.usingKey
		self.usingKey			= (nextIndex, nextKey)
				
		return nextKey
	
	# 获取当前密钥
	def getCurrentKey(self) -> str | None:
		
		"""
		获取当前正在使用的key
		有的时候返回key str
		没有的时候返回None
		"""
		
		# 对self.usingKey解包 获取当前引索/key
		currentIndex, currentKey = self.usingKey
		
		return currentKey
	
	# 添加密钥
	def addKey(
		self,
		key: str
	) -> None:
		
		"""添加密钥"""
		
		self._keysList.append(key)
		
		return None
	
	# 删除特定密钥
	def removeKey(
		self,
		key: str
	) -> None:
		
		self._keysList.remove(key)
		
		return None