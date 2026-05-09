# ExceptionHandlerAction

异常处理动作常量。

## 常量定义

| 常量 | 值 | 含义 |
|------|-----|------|
| `CONTINUE` | `"continue"` | 继续执行 |
| `ABORT` | `"abort"` | 终止请求 |
| `RETRY` | `"retry"` | 稍后重试 |

## 使用场景

通常由 `ApiRequestExceptionHandler` 返回，供 `safeRequest` 等上层逻辑判断下一步动作。

```python
from aioverse.const import ExceptionHandlerAction

if action == ExceptionHandlerAction.RETRY:
    ...
elif action == ExceptionHandlerAction.ABORT:
    ...
```
