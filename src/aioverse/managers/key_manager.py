# 类型注解
from typing import List


class KeyManager:
	
	"""密钥管理"""
		
	__slots__ = ["_keys_list", "using_key"]
	
	def __init__(
		self,
		keys_list: List[str]
	):
		
		# 防止出现None的情况 先对列表进行格式化
		self._keys_list = [
			key
			for key in keys_list
			if isinstance(key, str) # 仅允许字符串类型的密钥
		]
		
		# 当前引索/密钥
		self.using_key  = (-1, None)
	
	def __str__(self) -> str:
		
		return "->".join(self._keys_list)
		
	def __len__(self) -> int:
		
		return len(self._keys_list)
	
	# 获取下一个密钥
	def get_next_key(self) -> str:
		
		"""
		获取下一个Key
		没有则抛出RuntimeError
		"""
		
		# 解包self.using_key 获取当前引索/key
		current_index, using_key	= self.using_key
		next_index					= current_index + 1
		
		"""
		只需要判断是否需求数量少于引索即可
		列表里只有key了
		"""
		if len(self._keys_list) - 1 < next_index: 
			
			raise RuntimeError("没有Key可继续使用")
		
		# 存在则获取该key
		next_key		= self._keys_list[next_index]
		# 更换self.using_key
		self.using_key	= (next_index, next_key)
				
		return next_key
	
	# 获取当前密钥
	def get_current_key(self) -> str | None:
		
		"""
		获取当前正在使用的key
		有的时候返回key str
		没有的时候返回None
		"""
		
		# 对self.using_key解包 获取当前引索/key
		current_index, current_key = self.using_key
		
		return current_key
	
	# 获取可用key
	def get_available_key(self) -> str | None:
	
		return self.get_current_key() or self.get_next_key()
	
	# 添加密钥
	def add_key(
		self,
		key: str
	) -> None:
		
		"""添加密钥"""
		
		self._keys_list.append(key)
		
		return None
	
	# 删除特定密钥
	def remove_key(
		self,
		key: str
	) -> None:
		
		self._keys_list.remove(key)
		
		return None