from abc import ABC, abstractmethod


class LogWriteProtocol(ABC):
	
	"""
	日志写入接口
	"""
	
	# 必须实现的write
	@abstractmethod
	def write(self, text: str) -> None:
		
		"""
		写入日志
		"""
		
		pass