"""
测试上下文组装
"""
from aioverse.types import Content, Context, ContentArray

# 基础正文
text = Content(
	"text",
	"你好"
)
# 附件
file = Content(
	"image_url",
	{"url": "cxk"}
)

# 组装列表
contents = ContentArray()

contents.addContent(text).addContent(file)

# 组装上下文