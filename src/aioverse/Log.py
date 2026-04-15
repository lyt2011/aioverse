"""
日志系统
"""
# 时间获取
from datetime import datetime
# 类型注解
from typing import Callable, Awaitable, Tuple, Optional
# 导入接口
from aioverse.models.protocols import LogProtocol, LogWriteProtocol, LogFormatProtocol
# 异步实现
import asyncio
# 异步文件实现
import aiofiles


class BaseLog(LogProtocol):
	
	"""
	注意，不提供记录
	继承Log协议接口
	作为Log基类
	"""
	
	def __init__(
		self,
		formatter : LogFormatProtocol,
		writer    : LogWriteProtocol
	):
		
		self.formatter = formatter
		self.writer    = writer

class BaseWriter(LogWriteProtocol):
	
	"""
	不提供写入
	继承Writer协议接口
	作为任意Writer的基类
	"""
	def __init__(
		self,
		logFileName : str = "log.log",
		bufSize     : int = 10
	):
		
		"""
		args:
			logFileName 日志名 str
			bufSize 缓冲区大小，越小越实时，越大性能越好 int
		"""
		
		self.fileName   = logFileName
		
		# 缓冲蛆
		self._logBuffer = []
		self.bufSize    = bufSize
	
	# def write(self, *args, **kwargs): pass
	"""
	这里疏忽了，再次定义一个writer函数会把协议的write给重写
	导致出现了绕过协议类型检查的可能
	"""
	

class LogFormatter(LogFormatProtocol):
	
	"""负责格式化日志"""
	
	def __init__(
		self,
		source	: str = ""
	):
		
		self.source = source
	
	def format(
		self,
		text  : str,
		time  : str,
		level : str = "Info"
	) -> Tuple[str, str]:
		
		"只负责生成一个可阅读的字符串并返回"
			
		if (
			not isinstance(text,  str) or
			not isinstance(level, str) or
			not isinstance(time,  str)
		): raise TypeError(
			f"错误的数据类型: "
			f"text: {type(text)} "
			f"level: {type(level)} "
			f"time: {type(time)} "
			"内有一个不为str"
		)
		
		# 格式化level 便于处理
		level = level.lower()
		
		match level:
		
			case "info"	: color = "\033[32m"
			
			case "warn"	: color = "\033[33m"
			
			case "error": color = "\033[31m"
			
			case "debug": color = "\033[36m"
			
			case _		: color = "\033[0m" # 别的就默认白色
		
		noColorText = f"[{time} {level} {self.source}] > {text}\n" # 供给日志写入
		colorText   = f"{color}{noColorText}\033[0m" # 恢复后续正常颜色
		
		return noColorText, colorText
		


class AsyncWriter(BaseWriter):
	
	"""负责异步写入"""
	
	async def write(self, text: str) -> None:
		
		"""
		每次调用write都是加入缓冲区
		当缓冲区消息条数大于等于bufSize时
		清空缓冲区并用""连接，一起写入
		毕竟一直open，手机迟早报废😱😱😱
		"""
		if not text: return None
		
		self._logBuffer.append(text)
		
		if len(self._logBuffer) >= self.bufSize:
			
			# 连接缓冲区内所有信息
			textFormatted = "".join(self._logBuffer)
		
			async with aiofiles.open(self.fileName, "a") as file:
				
				await file.write(f"{textFormatted}")
			
			# 清空缓冲区
			self._logBuffer.clear()
			
		return None

class SyncWriter(BaseWriter):
	
	"""
	负责同步写入
	66，之前为什么不继承AsyncWriter
	还得多写一次init😱😱😱
	"""
	
	def write(self, text: str) -> None:
		
		"""
		重写AsyncWriter.write
		实现方法一致
		不过是用同步的方式写入
		"""
		
		if not text: return None
		
		self._logBuffer.append(text)
		
		if len(self._logBuffer) >= self.bufSize:
			
			textFormatted = "".join(self._logBuffer)
		
			with open(self.fileName, "a") as file:
				
				file.write(f"{textFormatted}")
			
			self._logBuffer.clear()
		
		return None


class AsyncLog(BaseLog):
	
	"""负责异步处理日志"""
		
	async def log(
		self,
		text  : str,
		level : str = "Info"
	) -> None:
		
		"""
		对LogFormatter, AsyncWriter
		进行高级的封装
		"""
		
		# 生成日志
		logText, logTextColor = self.formatter.format(
			time  = str(datetime.now()),
			text  = text,
			level = level
		)
		
		# 显示日志
		print(logTextColor) # 显示有颜色的
		
		# 写入日志
		await self.writer.write(f"{logText}\n") # 写入没颜色的
		
		return None

class SyncLog(BaseLog):
	
	"""
	哎哟，之前怎么没想到继承AsyncLog！现在使用BaseLog作为基类！
	又又多写一次init
	😱
	"""
	
	def log(
		self,
		text  : str,
		level : str = "Info"
	) -> None:
		
		"""
		AsyncLog.log的同步实现
		效果一致
		"""
		
		# 格式化日志
		logText, logTextColor = self.formatter.format(
			time  = str(datetime.now()),
			text  = text,
			level = level
		)
		
		print(logTextColor)
		
		self.writer.write(f"{logText}\n")
		
		return None
		
if __name__ == "__main__":
	
	sw = SyncWriter("test.log", bufSize=5) # 触发写入测试
	lf = LogFormatter()
	
	sl = SyncLog(
		formatter=lf,
		writer=sw
	)
	
	sl.log(text="测试日志", level="Info")
	sl.log(text="测试日志", level="Warn")
	sl.log(text="测试日志", level="Debug")
	sl.log(text="测试日志", level="Error")
	sl.log(text="测试日志", level="Other")