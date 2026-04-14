# 类型注解
from typing import Dict, Optional
# 结构体
from dataclasses import dataclass
# 群上下文结构体
from aioverse.models.structs import GroupContext
# 系统控制
import os
# 异步文件读取
import aiofiles
# json实现
import json


# 群上下文管理器
class GroupContextManager:
	
	"""
	当被实例化时作为一个总的群上下文管理器
	"""
	
	def __init__(
		self,
		groupContextDict: Optional[Dict[int, GroupContext]] = None
	):
		
		# 群上下文
		self._groupContext: Dict[int, GroupContext] = {}
		
		# 如果有上下文传入则更新
		if groupContextDict: self.fromDict(groupContextDict)
	
	# 长度获取
	def __len__(self) -> int:
		
		return len(self._groupContext)
	
	# str()
	def __str__(self) -> str:
		
		return str(len(self._groupContext))
	
	# repr()
	def __repr__(self) -> str:
		
		return f"共 {len(self._groupContext)} 个对象"
	
	# 获取群上下文
	def getGroupContext(
		self,
		groupId: int
	) -> GroupContext | None:
		
		return self._groupContext.get(groupId)
	
	# 创建群上下文
	def createGroupContext(
		self,
		groupId: int,
		groupContext: Optional[GroupContext] = None
	) -> GroupContext:
		
		# 创建一个新的上下文管理器
		if not groupContext:
			
			groupContext = GroupContext()
		
		self._groupContext[groupId] = groupContext
		
		return groupContext
	
	# 获取一个群号是否含有上下文
	def hasContext(
		self,
		groupId: int
	) -> bool:
		
		"""
		判断群是否含有上下文
		"""
		
		return groupId in self._groupContext
	
	# 转为字典
	def toDict(self) -> Dict[int, GroupContext]:
		
		"""
		顾名思义转为字典
		"""
		
		return self._groupContext
	
	# 从字典更新上下文
	def fromDict(
		self,
		data: Dict[int, GroupContext]
	) -> None:
		
		"""
		当前格式
		群号: GroupContext
		
		那么我直接update应该没问题
		"""
		
		self._groupContext.update(data)
		
		return None
	
	# 从文件加载群聊的上下文
	@staticmethod
	async def loadGroupContext(filePath: str) -> Optional[Dict[int, GroupContext]]:
		
		"""
		读取上下文文件 并获取内容
		
		
		"""
		
		# 打开文件 并读取
		async with aiofiles.open(filePath) as file:
				
			# 这时候读取的是字符串
			contextString = await file.read()
			
		# 对上下文字符串进行编译 获取上下文
		contextDict		= json.loads(contextString)
		
		# 获取工具上下文 角色扮演上下文 返回"{}"防止报错
		roleContextList	= contextDict.get("role", {})
		toolContextList	= contextDict.get("tool", {})
		
		# 实例化群组上下文
		groupContext	= GroupContext(
			roleContext	= roleContextList,
			toolContext	= toolContextList
		)
		
		return groupContext
			
	
	# 保存一个群聊上下文
	@staticmethod
	async def saveGroupContext(
		filePath		: str,
		groupContext	: GroupContext
	) -> None:
		
		"""
		保存对应群聊上下文
		
		错误仅会输出日志
		不抛出
		"""
		
		# 把工具ai 角色扮演ai上下文分别转为列表
		toolContextList = groupContext.toolContext.toList()
		roleContextList = groupContext.roleContext.toList()
		
		# 编译上下文为Json数组
		contextJson		= json.dumps(
			{
				"tool": toolContextList,
				"role": roleContextList
			},
			ensure_ascii=False
		)
			
		# 打开文件
		async with aiofiles.open(filePath, "w") as file:
			
			# 写入文件
			await file.write(contextJson)

		return None