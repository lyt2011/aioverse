# 类型两件套
from pydantic import BaseModel, ConfigDict
from typing import Dict, Literal


# 基础多模态信息
class Segment(BaseModel):
	
	type: str
	data: str
	
	def __len__(self) -> int:
		
		return len(self.data) * 1
	
	def to_dict(self) -> Dict[str, str]:
		
		return {
			"type"		: self.type,
			self.type	: self.data
		}

# 文本多模态
class Text(Segment):
	
	type: Literal["text"] = "text"
	
# 图片url多模态
class ImageUrl(Segment):

	type: Literal["image_url"] = "image_url"