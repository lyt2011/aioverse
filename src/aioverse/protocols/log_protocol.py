from abc import ABC, abstractmethod


class LogProtocol(ABC):
	
	"""
	日志接口
	"""
	
	# 必须实现的log方法
	@abstractmethod
	def log(self, text: str) -> None:
		
		"""
		操作日志
		"""
		
		pass