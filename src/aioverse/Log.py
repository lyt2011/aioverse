"""
日志系统
"""
# 时间获取
from datetime	import datetime
# 类型注解
from typing		import Callable, Awaitable, Tuple, Optional

# 导入接口
from aioverse.protocols import LogProtocol, LogWriteProtocol, LogFormatProtocol

# 异步实现
import asyncio
# 异步文件实现
import aiofiles
# 系统控制
import sys


# 全局日志实例存储
_global_logs = {}


class BaseLog:
	
	def __init__(
		self,
		formatter : LogFormatProtocol,
		writer    : LogWriteProtocol
	):
		
		self.formatter = formatter
		self.writer    = writer

class BaseWriter:
	
	def __init__(
		self,
		file_name	: str,
		buffer_size	: int = 10
	):
		
		self.file_name	= file_name
		
		# 缓冲蛆
		self._log_buffer	= []
		self.buffer_size	= buffer_size

class LogFormatter(LogFormatProtocol):
	
	"""负责格式化日志"""
	
	def __init__(
		self,
		source: str
	):
		
		self.source = source
	
	def format(
		self,
		text  : str,
		time  : str,
		level : str = "Info"
	) -> Tuple[str, str]:
		
		"只负责生成一个可阅读的字符串并返回"
		
		# 格式化level 便于处理
		level = level.lower()
		
		match level:
		
			case "info"			: color = "\033[96m"
			
			case "warn"			: color = "\033[33m"
			
			case "error"		: color = "\033[31m"
			
			case "debug"		: color = "\033[36m"
			
			case "successful"	: color = "\033[092m"
			
			case _				: color = "\033[0m" # 别的就默认白色
		
		no_color_text	= f"[{time} {level} {self.source}] > {text}\n" # 供给日志写入
		color_text		= f"{color}{no_color_text}\033[0m" # 恢复后续正常颜色
		
		return no_color_text, color_text

class AsyncWriter(BaseWriter, LogWriteProtocol):
	
	"""负责异步写入"""
	
	async def write(
		self,
		text	: str,
		flush	: bool = False
	) -> None:
		
		if not text: return None
		
		self._log_buffer.append(text)
		
		if (
			len(self._log_buffer) >= self.buffer_size
			or flush is True
		):
			
			# 连接缓冲区内所有信息
			text_formatted = "".join(self._log_buffer)
		
			async with aiofiles.open(self.file_name, "a") as file:
				
				await file.write(f"{text_formatted}")
			
			# 清空缓冲区
			self._log_buffer.clear()
			
		return None

class SyncWriter(BaseWriter, LogWriteProtocol):
	
	def write(
		self,
		text	: str,
		flush	: bool = False
	) -> None:
		
		"""
		重写AsyncWriter.write
		实现方法一致
		不过是用同步的方式写入
		"""
		
		if not text: return None
		
		self._log_buffer.append(text)
		
		if (
			len(self._log_buffer) >= self.buffer_size
			or flush is True
		):
			
			text_formatted = "".join(self._log_buffer)
		
			with open(self.file_name, "a") as file:
				
				file.write(f"{text_formatted}")
			
			self._log_buffer.clear()
		
		return None


class AsyncLog(BaseLog, LogProtocol):
	
	"""负责异步处理日志"""
		
	async def log(self, text: str, level: str = "Info", flush: bool = False):
		
		"""
		对LogFormatter, AsyncWriter
		进行高级的封装
		"""
		
		# 生成日志
		log_text, color_log_text = self.formatter.format(
			time  = str(datetime.now()),
			text  = text,
			level = level
		)
		
		# 显示日志
		sys.__stdout__.write(color_log_text) # 显示有颜色的
		sys.__stdout__.flush()
		
		# 写入日志
		await self.writer.write(text=log_text, flush=flush)
		
		return None

class SyncLog(BaseLog, LogProtocol):
	
	def log(self, text: str, level: str = "Info", flush: bool = False):
		
		"""
		AsyncLog.log的同步实现
		效果一致
		"""
		
		# 格式化日志
		log_text, color_log_text = self.formatter.format(
			time  = str(datetime.now()),
			text  = text,
			level = level
		)
		
		sys.__stdout__.write(color_log_text) # 显示有颜色的
		sys.__stdout__.flush()
		
		self.writer.write(text=log_text, flush=flush)
		
		return None
		
# 便捷的日志获取
def get_log(
	file_name	: str,
	source		: str,
	is_async	: bool = False
) -> BaseLog:
	
	"""
	除了文件名与来源
	其他全部采用默认值
	"""
	
	# 日志实例标识符
	log_sign	= (file_name, source, is_async)
	
	# 判断是否已经创建了相同日志实例
	if log_sign in _global_logs: return _global_logs[log_sign]
	
	# 格式化函数不支持异步 单独创建
	formatter	= LogFormatter(source)

	log_ob	= AsyncLog(
		writer		= AsyncWriter(file_name),
		formatter	= formatter
	) if is_async else SyncLog(
		writer		= SyncWriter(file_name),
		formatter	= formatter
	)
	
	# 否则创建
	_global_logs[log_sign] = log_ob
	
	return log_ob