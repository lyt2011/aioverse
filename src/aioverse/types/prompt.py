from .context import Context


# 注意role一般不支持多模态 (就算API允许注意力也不会放在多模态上)
class Prompt(Context):
	
	def __init__(
		self,
		content: str
	):
		
		super().__init__(
			role	= "system",
			content	= content
		)