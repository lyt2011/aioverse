from .base_context	import Context

from typing	import Literal


class User(Context):
	
	role: Literal["user"] = "user"
