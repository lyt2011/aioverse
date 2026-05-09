# 🚀快速开始

## 环境配置
```bash
git clone https://github.com/lyt2011/aioverse
cd aioverse
pip install .
```

## 代码示例

### Content (上下文正文)
```python
from aioverse.types import Content

text_content		= Content("text", "你好")
image_url_content	= Content("image_url", {"url": "cxk.com/picture.png"})

print(text_content.toDict())		# {"type": "text", "text": "你好"}
print(image_url_content.toDict())	# {"type": "image_url", "image_url": {"url": "cxk.com/picture.png"}}
```

### ContentArray (上下文正文数组)
```python
from aioverse.types import ContentArray, Content

content_array = ContentArray()

# 显式传参
content_array.addData("text", "你好")
print(content_array.toList()) # [{"type": "text", "text": "你好"}]

# 通过Content (上下文正文)添加
content = Content("text", "你很好")
content_array.addContent(content)
print(content_array.toList())
# [
# 	{"type": "text", "text": "你好"},
# 	{"type": "text", "text": "你很好"}
# ]

# 通过引索插入
content2 = Content("text", "咕咕嘎嘎")
content_array.addContent(content2, index=1)
print(content_array.toList())
# [
# 	{"type": "text", "text": "你好"},
# 	{"type": "text", "text": "咕咕嘎嘎"},
# 	{"type": "text", "text": "你很好"}
# ]
```

### Context (上下文对象)
```python
from aioverse.types import ContentArray, Context

# 接受Context对象
content = Content("text", "你好")
context = Context("user", content)
print(context.toDict())
# {
# 	"role": "user",
# 	content: [
# 		{"type": "text", "text": "你好"}
# 	]
# }

# 接受纯字符串
context = Context("user", "你好")
# {
# 	"role": "user",
# 	"content": "你好"
# }
```

# aioverse.types
- `Content`: 上下文正文对象
- `ContentArray`: 上下文正文数组对象
- `Context`: 上下文对象
- `Item`: 一般用来作为动态容器
- `Prompt`: 提示词，完全继承`Content`，但是默认`role`为`system`