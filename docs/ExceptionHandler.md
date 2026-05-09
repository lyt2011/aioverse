# ExceptionHandler 模块

为 API 请求异常提供可扩展的处理策略。

## ApiRequestExceptionHandler

基于错误码分发的异常处理器。

### 构造函数

```python
from aioverse.ExceptionHandler import ApiRequestExceptionHandler

handler = ApiRequestExceptionHandler()
```

### __call__

```python
action = handler(error: ResponseCodeError) -> str | None
```

返回值为 `ExceptionHandlerAction` 常量之一：
- `RETRY` - 建议重试
- `ABORT` - 终止请求
- `None` - 未定义该错误码的处理器

### setHandler

注册自定义错误码处理器。

```python
def my_handler(code, response):
    return "abort"

handler.setHandler("500", my_handler)
```

### deleteHandler

删除已注册的错误码处理器。

```python
handler.deleteHandler("500")
```

## 内置策略

| 错误码 | 策略 | 说明 |
|--------|------|------|
| `429` | 智能判断 | 若响应元数据包含 `headers`，视为配额耗尽（`ABORT`）；否则为请求过多（`RETRY`）。 |

## 使用示例

```python
from aioverse.ExceptionHandler import ApiRequestExceptionHandler
from aioverse.errors import ResponseCodeError

handler = ApiRequestExceptionHandler()

try:
    ...
except ResponseCodeError as e:
    action = handler(e)
    if action == "retry":
        print("稍后重试")
    elif action == "abort":
        print("终止流程")
```
