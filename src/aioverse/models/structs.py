"""

顾名思义就是放结构体的
python叫dataclass

"""

# 类型注解
from typing import Optional, Any, List, Dict, Tuple, Callable
# 结构体
from dataclasses import dataclass
# 抽象接口
from aioverse.models.protocols import ContextManagerProtocol

# json实现
import orjson


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

# 普通上下文
@dataclass(frozen=True)
class Context:
	
	# 角色
	role	: str
	# 正文
	content	: Any
	
	def toDict(self) -> Dict[str, str]:
		
		# 正常来说 一般有解析结束后都有这个变量 但以防万一
		contentString = None
		
		# 判断正文内容类型 不是字符串
		if not isinstance(self.content, str):
			
			# 优先使用toString方法
			if hasattr(self.content, "toString"):
			
				contentString = self.content.toString()
			
			# 兜底尝试调用self.content的__str__方法
			else:
				
				contentString = str(self.content)
		
		# 否则直接赋值即可
		else: contentString = self.content
				
		# 解析失败
		if contentString is None:
			
			raise ValueError(
				f"无法将 {self.content}"
				f"({type(self.content)})"
				f"转为字符串"
			)
		
		return {"role": self.role, "content": contentString}

# 提示词 直接继承context
class Prompt(Context):
	
	def __init__(self, content: Any):
		
		super().__init__(
			role	= "system",
			content	= content
		)

# 物件 对信息的封装 便于调用
class Item:
	
	def __init__(
		self,
		_default_result: Optional[Any] = None,
		**kwargs
	):
		
		# 默认返回值
		self._default_result	= _default_result
		
		for key, value in kwargs.items():
			
			# 判断是否可能为关键方法
			if key.startswith("__") and key.endswith("__"):
				
				raise TypeError(f"不可修改关键方法 ({key})")
			
			setattr(self, key, value)
		
		# 这个kwargs便于转字典
		self._kwargs			= kwargs
	
	def __getattr__(self, name: str) -> None:
		
		"""
		这里直接返回none
		因为能运行这个函数证明已经是不存在了
		"""
		
		return self._default_result
	
	def toDict(self) -> Dict[str, Any]:
		
		return self._kwargs
	
	def toString(self) -> str:
		
		return orjson.dumps(self.toDict()).decode("utf-8")