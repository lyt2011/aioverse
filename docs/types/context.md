# Context

表示单条对话上下文（角色 + 内容）。

## 构造函数

```python
from aioverse.types import Context, ContentArray

ctx = Context(
    role="user",                    # system / user / assistant
    content="你好",                  # str 或 ContentArray
    token=None                      # 可选，自定义 token 数
)
```

## 方法

| 方法 | 说明 |
|------|------|
| `toDict()` | 返回 OpenAI 协议格式字典 |
| `setToken(count)` | 设置自定义 token 数 |
| `__len__()` | 无自定义 token 时返回内容长度；否则返回 token 数 |
