# 类型两件套
from pydantic import BaseModel, model_validator
from typing import List, Optional, Dict, Any

from .assistant_key	import AssistantKey


class ModelConfig(BaseModel):
	
	model_name	: str
	model_alias	: str
	
	api_url		: str
	model_keys	: List[AssistantKey]
	
	max_token	: int = 0
	token_limit	: int = 0
	
	support_image	: bool = False # 支持图片理解
	support_video	: bool = False # 支持视频理解
	support_audio	: bool = False # 支持音频理解
	
	support_tool	: bool = False # 支持工具调用
	support_think	: bool = False # 支持推理
	
	def __str__(self) -> str:
		
		return f"{self.model_name}:{self.model_alias}:{self.api_url}"
	
	def __repr__(self) -> str:
		
		return self.__str__()
	
	# 实例化完成前
	@model_validator(mode="before")
	@classmethod
	def _verify_before(
		cls,
		data: Dict[str, Any]
	) -> Dict[str, Any]:
		
		model_alias	= data.get("model_alias")
		model_name	= data.get("model_name")
		
		if not model_alias and model_name:
			
			# 使用model_name作为默认别名
			data["model_alias"] = model_name
		
		return data

	# 实例化完成后
	@model_validator(mode="after")
	def _verify_after(self) -> "self":
		
		if len(self.model_keys) < 1:
			
			raise ValueError("至少需要一个可用密钥")
		
		return self