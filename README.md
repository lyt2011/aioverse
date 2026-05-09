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
```
- 显式传参
```python
content_array.addData("text", "你好")
print(content_array.toList()) # [{"type": "text", "text": "你好"}]
```
- 通过Content (上下文正文)添加
```python
content = Content("text", "你很好")
content_array.addContent(content)
print(content_array.toList())
# [
# 	{"type": "text", "text": "你好"},
# 	{"type": "text", "text": "你很好"}
# ]
```
- 通过引索插入
```python
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

# 模块说明

## aioverse.types
- `Content`: 上下文正文对象
- `ContentArray`: 上下文正文数组对象
- `Context`: 上下文对象
- `Item`: 一般用来作为动态容器
- `Prompt`: 提示词，完全继承`Content`，但是默认`role`为`system`

## aioverse.managers

### KeyManager (密钥管理器)
```python
from aioverse.managers import KeyManager

keys = ["密钥1", "密钥2"]

# 接受一个List[str]
key_manager = KeyManager(keys)
```
- 为了防止引索超界 默认引索为-1 所以需要getNextKey()初始化
- `getNextKey()` 会设置当前引索为下一个密钥的引索
```python
key_manager.getNextKey() # "密钥1"
```
- 获取当前密钥
```python
key_manager.getCurrentKey() # "密钥1"
```
- 也可以通过`getAvailableKey`方法获取可用Key
- 自动调用`getCurrentKey`方法
- 若结果为`None` 继续调用`getNextKey`方法
- **若没有key可获取还是会报错**
```python
key_manager.getAvailableKey() # "密钥1"
```
- 一直获取下一个
```python
key_manager.getNextKey()
# key_manager.getNextKey() <- RuntimeError("没有可用的Key")
```
- 添加密钥
```python
key_manager.addKey("密钥114514")
```
- 删除密钥
```python
key_manager.removeKey("密钥114514")
```
- 具体可以查看`aioverse/managers/key_manager.py`

### ContextManager (上下文管理器)
- 通过初始化传参`context_array`添加
```python
from aioverse.managers import ContextManager
from aioverse.types import Context

# 创建上下文对象列表
context_array = [
	Context("system", "你是一个AI助手..."),
	Context("user", "你好")
]

# 接受一个可选的上下文对象列表List[Context]
context_manager = ContentManager(context_array)
```
- 或者通过`addContext`方法手动添加
```python
context_manager = ContentManager()
for context in context_array:
	context_manager.addContext(context)
```
- 转为列表
```python
context_manager.toList()
[
	{"role": "system", "content": "你是一个AI助手..."},
	{"role": "user", "content": "你好"}
]
```
- 更多接口可以查看`aioverse/managers/context_manager.py`

### JsonManager
- 继承`dict`，提供了一些封装，没有黑魔法
- 具体可以查看`aioverse/managers/json_manager.py`

## aioverse.OpenAI
- 基于`aiohttp`
- 将请求封装为兼容`OpenAI API`的格式
- 太晚了不写了累了
