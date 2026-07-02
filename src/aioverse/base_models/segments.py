# 类型两件套
from pydantic import BaseModel, ConfigDict
from typing import Dict, Literal, Optional, Any

import orjson


# 基础多模态信息 TODO 这里缺少反序列化
class Segment(BaseModel):
	
	type: str
	data: str
	
	def model_dump(self) -> Dict[str, str]:
		
		return {"type": self.type, self.type: self.data}
	
	def model_dump_json(self) -> str:
		
		return orjson.dumps(self.model_dump()).decode()

# 文本多模态
class Text(Segment):
	
	type: Literal["text"] = "text"
	
# 图片url多模态
class ImageUrl(Segment):

	type: Literal["image_url"] = "image_url"

# 音频输入多模态
class AudioInput(Segment):
	
	"""音频输入较特殊 需要重写"""
	
	type	: Literal["audio_input"]	= "audio_input"
	format	: Optional[str]				= "mp3"
	data	: str
	
	def model_dump(self) -> Dict[str, Any]:
		
		return {
			"type"		: self.type,
			self.type	: {"data": self.data, "format": self.format}
		}