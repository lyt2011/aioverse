from dataclasses import dataclass
from typing import Optional, Any

@dataclass
class Error:
	
	"""
	错误的基类 (仅用于存放数据 不用于raise)
	包含错误码 错误信息 源信息
	"""
	
	# 错误码
	code		: Optional[int] = None
	# 错误信息
	message		: Optional[str] = None
	# 源信息
	metaData	: Optional[Any] = None