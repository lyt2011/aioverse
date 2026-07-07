from .base_segment	import Segment

from typing	import Literal


# 文本多模态
class Text(Segment):
	
	type: Literal["text"] = "text"