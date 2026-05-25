# 工具实现
from aioverse.models.tool_schema import Tool
# 工具实现(AI返回)
from aioverse.models.tool_call_response import ToolCall
# 工具调用结果
from aioverse.models.contexts import ToolExecuteResult

# 类型注解
from typing import Dict, Tuple, List, Any

# 异步实现
import asyncio


class ToolManager:
	
	"""为AI工具实现便捷的调用与存储"""
	
	__slots__ = ["schema"]
	
	def __init__(self):
		
		self.schema: Dict[str, Tuple[callable, Tool]] = {}
	
	def register(
		self,
		func	: callable,
		scheme	: Tool
	) -> None:
		
		"""自动通过func的__name__作为键"""
		
		self.schema[func.__name__] = (func, scheme)
		
		return None
	
	# 实现工具执行器
	async def tool_executer(
		self,
		tool_calls: List[ToolCall]
	) -> List[ToolExecuteResult]:
		
		"""
		想了两年半 返回构建好的ToolExecuteResult
		因为如果直接返回工具调用结果的话
			调用方还需要通过tool_calls的id对应列表的每一个结果手动构建ToolExecuteResult
			比较麻烦？
		"解耦是为了**更好的维护**而**不是为了更难的调用**" -- 鲁迅•《汉谟拉比法典》
		"""
		
		async def safe_run_coro(coro) -> Any:
			
			"""安全地执行协程 错误会当成字符串返回"""
			try: return await coro
			except Exception as e: return f"{type(e).__name__}: {str(e)}"
		
		# 协程对象字典
		coros	= {}
		# 执行结果
		results: List[ToolExecuteResult] = []
		
		# 将同步与异步函数均转为协程对象
		for tool_call in tool_calls:
			
			# 先通过name找到已注册的函数
			func, _ = self.schema[tool_call.function.name]
			
			# 转协程对象
			coro = (
				func(**tool_call.function.arguments)
				if asyncio.iscoroutinefunction(func)
				else asyncio.to_thread(func, **tool_call.function.arguments)
			)
			
			# 添加进入协程对象字典
			coros[tool_call.id] = coro
		
		# 这里为什么不用asyncio.gather？
		# 因为asyncio.gather是完全并发的
		# 当一个工具依赖前一个工具的执行结果时
		# gather会导致前置工具未执行完毕就直接执行该工具 出现bug
		# 如请求文件写入了但是读取是空白的 甚至报错
		# 直接await更便于构建ToolExecuteResult
		for tool_call_id, coro in coros.items():
			
			# 构建ToolExecuteResult
			execute_result = ToolExecuteResult(
				tool_call_id= tool_call_id,
				content		= await safe_run_coro(coro)
			)
			
			results.append(execute_result)
		
		return results
	
	# 转为Openai标准的tools
	def to_list(self) -> List[Tool]:
		
		return [
			tool.to_dict()
			for _, tool in self.schema.values()
		]