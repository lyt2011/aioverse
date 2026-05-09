# Content

表示 OpenAI 消息内容协议中的单个内容单元。

## 构造函数

```python
from aioverse.types import Content

content = Content(
    content_type="text",          # 类型: text / image_url
    content_data="Hello world"    # 实际内容
)
```

## 方法

| 方法 | 说明 |
|------|------|
| `toDict()` | 返回 `{"type": ..., "text": ...}` 格式字典 |
| `__len__()` | 返回内容字符串长度 |
