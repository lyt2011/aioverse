"""

顾名思义就是放结构体的
python叫dataclass

"""

# 类型注解
from typing import Optional, Any
# 结构体
from dataclasses import dataclass
# 抽象接口
from aioverse.models.protocols import ContextManagerProtocol


# 一种错误 注意这不能用来raise
@dataclass
class Error:
	
	"""
	包含错误码 错误信息 源信息
	"""
	
	# 错误码
	code		: Optional[int] = None
	# 错误信息
	message		: Optional[str] = None
	# 源信息
	metaData	: Optional[Any] = None

# 结构体
@dataclass
class GroupContext:
	
	"""
	群组上下文
	
	包含工具 角色扮演
	"""
	
	# 角色扮演上下文
	roleContext: Optional[ContextManagerProtocol] = None
	# 工具调用上下文
	toolContext: Optional[ContextManagerProtocol] = None
