# ResponseCodeError

API 返回码异常，当 HTTP 状态码非 200 时抛出。

## 构造函数

```python
from aioverse.errors import ResponseCodeError

raise ResponseCodeError(
    code=429,
    response={"error": "Too Many Requests"}
)
```

## 字段

| 字段 | 说明 |
|------|------|
| `code` | HTTP 状态码 |
| `response` | 服务端返回的原始响应体 |

## 字符串表示

```python
str(error)  # "429: {'error': 'Too Many Requests'}"
```
