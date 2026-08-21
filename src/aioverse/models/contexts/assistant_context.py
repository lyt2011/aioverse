from .base_context	import BaseContext
from ...enums		import Roles

from typing	import Literal


class AssistantContext(BaseContext):

	"""Assistant 类型上下文"""

	role: Literal[Roles.ASSISTANT] = Roles.ASSISTANT