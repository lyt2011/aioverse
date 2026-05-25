# 类型两件套
from pydantic import BaseModel, model_validator
from typing import List


class ModelConfig(BaseModel):
	
	model_name	: str
	api_url		: str
	model_keys	: List[str]

	# 验证密钥列表数量
	@model_validator(mode="after")
	def verify_key_quantity(self) -> "self":
		
		if len(self.model_keys) < 1:
			
			raise ValueError("至少需要一个可用密钥")
		
		return self