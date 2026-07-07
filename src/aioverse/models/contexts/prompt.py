from .base_context	import Context

from typing	import Literal


class Prompt(Context):
	
	role: Literal["system"] = "system"