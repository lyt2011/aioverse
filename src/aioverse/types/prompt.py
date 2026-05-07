from .context import Context
from .content_array import ContentArray


class Prompt(Context):
	
	def __init__(
		self,
		content: ContentArray | str
	):
		
		super().__init__(
			role	= "system",
			content	= content
		)