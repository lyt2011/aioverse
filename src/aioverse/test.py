# 协议
from aioverse.models.protocols import OpenAIProtocol, ContextManagerProtocol
# AI工具 转换函数
from aioverse.AITools import toolExecuter, getClassFunction, functionToDict, AITools, extractTools


async def fullAIRequest(
	openAIClient: OpenAIProtocol,
	toolContext	: ContextManagerProtocol,
	roleContext	: ContextManagerProtocol
):

	"""
	请求完整流程
	"""
	
	# 阶段 1 获取可被调用的工具
	# 从AITools获取所有工具函数
	toolFunctions	= getClassFunction(AITools)
	# 转换每一个工具函数为字典
	toolDictList	= [functionToDict(toolFunction) for toolFunction in toolFunctions]
	
	# 阶段2 获取工具需求
	# 这里我就不演示了 大概就是json.loads(ai回复) 获取工具需求
	# 提示词限制的很紧 不用管格式是否正确先
	
	# 假设这是ai请求的工具
	tools			= [
		{
			"name": "searchOnline",
			"params": {"query": "1+1等于多少"}
		},
		{
			"name": "searchOnline",
			"params": {"query": "2+2等于多少"}
		}
	]
	
	# 阶段三 获取工具调用结果
	# 通过ai回复在AITools里获取工具
	toolFunctions	= extractTools(AITools, tools)
	# 执行工具
	toolCallResult	= await toolExecuter(toolFunctions)
	
	# 阶段4 把工具调用结果+用户输入插入角色扮演ai上下文里面
	# 依旧不演示 麻烦 大致过程跟工具ai差不多
	
	# 假设这是角色扮演ai回复
	response		= "114514"
	
	# 返回最终调用结果
	return response