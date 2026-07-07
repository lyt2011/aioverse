from .base_segment	import Segment

from typing	import Literal, Optional, Dict, Any


# 音频输入多模态
class AudioInput(Segment):
	
	"""音频输入较特殊 需要重写"""
	
	type	: Literal["audio_input"]	= "audio_input"
	format	: Optional[str]				= "mp3"
	data	: str
	
	def model_dump(self) -> Dict[str, Any]:
		
		return {
			"type"		: self.type,
			self.type	: {
				"data"	: self.data,
				"format": self.format
		}}