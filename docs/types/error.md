# Error

仅用于存放错误数据的 dataclass，**不用于 raise**。

## 构造函数

```python
from aioverse.types import Error

err = Error(
    code=429,
    message="请求过多",
    metaData={"retry_after": 1}
)
```

## 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | `Optional[int]` | HTTP 或业务错误码 |
| `message` | `Optional[str]` | 错误描述 |
| `metaData` | `Optional[Any]` | 原始响应或附加信息 |
