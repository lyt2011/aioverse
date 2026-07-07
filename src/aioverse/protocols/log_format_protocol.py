from abc import ABC, abstractmethod


class LogFormatProtocol(ABC):
	
	"""
	日志格式化接口
	"""
	
	# 必须实现的format方法
	@abstractmethod
	def format(self, text: str, level: str) -> str:
		
		"""
		对日志内容格式化
		"""
		
		...