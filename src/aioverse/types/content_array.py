from typing import List, Dict, Any, Optional

from .item import Item
from .content import Content


class ContentArray:
	
	__slots__ = ["_contentArray"]
	
	# 辅助方法 验证数据
	@classmethod
	def _verify_data(
		cls,
		data: List[Dict[str, Any]]
	) -> Item:
		
		"""
		验证正文内容是否符合规定
		返回包含元数据与验证结果的Item实例
		"""
		
		is_pass		= True
		has_text	= False
		has_image	= False
		has_unknown	= False
		length		= len(data)
		meta_data	= data
		
		for content in data:
			
			is_pass = is_pass and (
				len(content) == 2
				and "type" in content
				and content["type"] in content
			)
			
			# 不合格跳过检查
			if not is_pass: continue
			
			# 验证类型
			match content["type"]:
				
				case "text"		: has_text		= True
				case "image_url": has_image		= True
				case _			: has_unknown	= True
				
		# 封装结果
		result		= Item(
			is_pass		= is_pass		,
			has_text	= has_text		,
			has_image	= has_image		,
			has_unknown	= has_unknown	,
			length		= length		,
			meta_data	= data
		)
		
		return result
	
	@classmethod
	def from_list(
		cls,
		data: List[Dict[str, Any]]
	) -> "ContentArray":
		
		"""
		通过列表创建实例
		
		理想格式:
		[
			{"type": "text", "text": "666"},
			{"type": "image_url", "image_url": "http://synb.com"}
		]
		"""
		
		# 验证数据
		verifyResult = cls._verify_data(data)
		if not verifyResult.is_pass:
			
			raise ValueError("data非理想格式")
		
		# 创建正文列表
		contents = [
			Content(
				content_type = content["type"],
				content_data = content[content["type"]]
			)
			for content in data
		]
		
		# 返回实例化的实例
		return ContentArray(contents)		
	
	def __init__(
		self,
		contents: Optional[List[Content]] = None
	):
		
		self._contentArray: list	= contents or []
	
	def __len__(self) -> int:
		
		return sum([
			len(content)
			for content in self._contentArray
		])
		
	def toList(self) -> List[Dict[str, Any]]:
		
		# 直接遍历对每个数据进行toDict即可
		return [
			content.toDict()
			for content in self._contentArray
		]
	
	def addContent(
		self,
		type	: str,
		text	: str,
		index	: int | None = None
	) -> "self":
		
		# 否则实例化一个Content
		content			= Content(type, text)
		
		# 判断插入模式 默认值append
		if index is None: self._contentArray.append(content)
		else			: self._contentArray.insert(index, content)
		
		# 返回自身 链式调用
		return self
	
	# 获取状态
	@property
	def status(self) -> Item:
		
		return self._verify_data(self.toList())