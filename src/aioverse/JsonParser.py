# rust json解析实现
import orjson
# 字面量解析实现
import ast
# 类型注解
from typing import Any

	
def deepJsonParser(json: Any) -> Any:

	# 仅对字符串进行解析
	if isinstance(json, str):
		
		# 去空白字符
		json			= json.strip()
		
		try:
			
			return deepJsonParser(orjson.loads(json))
		
		except orjson.JSONDecodeError:
			
			try:
				
				# 尝试使用字面量解析
				return deepJsonParser(ast.literal_eval(json))
			
			except Exception as e: pass
		
		# 都解析失败直接返回自身
		return json
		
	# 字典直接对值解析
	elif isinstance(json, dict):
		
		return {
			key: deepJsonParser(value)
			for key, value in json.items()
		}
	
	# 列表直接对元素解析
	elif isinstance(json, list):
		
		return [
			deepJsonParser(value)
			for value in json
		]
	
	# 默认返回自己
	else: return json