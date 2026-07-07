from .base_segment	import Segment

from typing	import Literal


class ImageUrl(Segment):

	type: Literal["image_url"] = "image_url"