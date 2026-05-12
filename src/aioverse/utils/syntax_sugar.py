from aioverse.managers import ContextManager
from aioverse.types import Context, Content, ContentArray

from typing import List, Dict, Any


# 上下文构建语法糖
def build_contexts(data: List[Dict[str, Any]]) -> ContextManager:
	
	"""
	将OpenAI格式的字典上下文转为ContextManager
	"""
	
	# 批量构建上下文正文
	def build_contents(contents: List[Dict[str, Any]]) -> ContentArray:
		
		return ContentArray([
			Content.from_dict(content)
			for content in contents
		])
	
	# 构建完成的Context实例
	contexts = []
	
	# 遍历data 获取每一个Context所需的数据
	for context in data:
		
		# 取出便于检查类型
		content = context["content"]
		
		# 检查content的类型
		# 字符串则直接使用
		if isinstance(content, str): pass
		
		# 列表则通过build_contents转为ContentArray
		elif isinstance(content, list):
			
			# 直接更改原数据 便于转换
			context["content"] = build_contents(content)
		
		# 都不是则抛出报错
		else:
			
			raise TypeError(f"content的类型不能为{type(content)}")
		
		# 转为Context实例
		context_instance	= Context.from_dict(context)
		
		# 转为Context并添加进入contexts
		contexts.append(context_instance)
	
	# 转为上下文管理器并返回
	return ContextManager(contexts)