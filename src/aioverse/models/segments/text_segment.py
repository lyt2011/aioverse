from .base_segment	import BaseSegment

from typing	import Literal, Any, Dict


class TextSegment(BaseSegment):
	
	"""文本消息段"""
	
	type	: Literal["text"]	= "text"
	text	: str
	
	def do_serialize(self) -> Dict[str, Any]:
		
		"""返回 OpenAI 兼容格式: {"type": "text", "text": "..."}"""
		
		return {
			"type"	: "text",
			"text"	: self.text
		}
