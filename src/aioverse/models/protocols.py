# 基类接口
from abc import ABC, abstractmethod
# 类型注解
from typing import Optional, Dict, Any


# OpenAI协议
class OpenAIProtocol(ABC):
	
	# 必须实现的chatCompletion方法
	@abstractmethod
	async def chatCompletion(
		self,
		headers	: Optional[Dict[str, Any]]	= None,
		params	: Optional[Dict[str, Any]]	= None,
		body	: Optional[Dict[str, Any]]	= None,
		timeout	: int						= 90
	) -> str:
		
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
			AI回复
		"""
		
		pass

# 错误处理协议
class ExceptionHandlerProtocol(ABC):
	
	"""
	不管如何处理
	
	必须通过直接调用实例进行使用
	"""
	
	# 必须实现通过实例直接使用
	@abstractmethod
	def __call__(self, error) -> str | None:
		
		"""
		调用实例直接使用
		
		类似
		a = ExceptionHandler()
		a(0/0)
		
		返回处理结果
		"""
	
		pass

# 上下文管理器抽象接口
class ContextManagerProtocol(ABC):
	
	pass
	
# 密钥管理器抽象接口
class KeyManagerProtocol(ABC):
	
	"""
	密钥管理器
	"""
	
	@abstractmethod
	def getCurrentKey(self) -> str | None:
		
		"""
		获取当前使用的密钥
		"""
		
		pass
	
	@abstractmethod
	def getNextKey(self) -> str | None:
		
		"""
		获取下一个密钥
		"""
		
		pass
	
	@abstractmethod
	def addKey(
		self,
		key: str
	) -> None:
		
		"""
		添加密钥
		"""
		
		pass
	
	@abstractmethod
	def removeKey(
		self,
		key: str
	) -> None:
		
		"""
		删除特定密钥
		"""
		
		pass

class LogProtocol(ABC):
	
	"""
	日志接口
	"""
	
	# 必须实现的log方法
	@abstractmethod
	def log(self, text: str)                 -> None: pass

class LogWriteProtocol(ABC):
	
	"""
	日志写入接口
	"""
	
	# 必须实现的write
	@abstractmethod
	def write(self, text: str)              -> None: pass

class LogFormatProtocol(ABC):
	
	"""
	日志格式化接口
	"""
	
	# 必须实现的format方法
	@abstractmethod
	def format(self, text: str, level: str) -> None: pass