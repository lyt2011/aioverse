from abc import ABC, abstractmethod


class LogWriteProtocol(ABC):
	
	"""
	日志写入接口
	"""
	
	# 必须实现的write
	@abstractmethod
	def write(
		self,
		text	: str,
		flush	: bool = False
	) -> None:
		
		"""
		写入日志
		
		flush为True时强行写入缓冲区内容
		"""
		
		pass