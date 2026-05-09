# AITools 模块

为 AI Function Calling 提供函数反射、参数提取与并发执行能力。

## FunctionTools

静态工具类，用于提取 Python 函数的元信息。

### functionParamToDict

将函数签名转换为参数描述字典。

```python
from aioverse.AITools import FunctionTools

def add(a: int, b: int = 0) -> int:
    """加法"""
    return a + b

params = FunctionTools.functionParamToDict(add)
# {'a': {'type': '<class int>', 'default': None, 'required': True},
#  'b': {'type': '<class int>', 'default': 0, 'required': False}}
```

### functionToDict

将函数转换为 AI 工具描述格式。

```python
tool_desc = FunctionTools.functionToDict(add)
# {'name': 'add', 'description': '加法', 'params': {...}}
```

## getFunctionFromObject

获取对象中所有函数成员。

```python
from aioverse.AITools import getFunctionFromObject

methods = getFunctionFromObject(MyToolClass())
```

## toolExecuter

并发执行工具调用，支持同步函数与异步函数混用。

```python
from aioverse.AITools import toolExecuter

tools = [
    {"searchOnline": {"query": "Python"}},
    {"calculate": {"expr": "1+1"}}
]
results = await toolExecuter(tools, obj=tool_instance)
```

**参数**：
- `tools`: 工具调用列表，每个元素为 `{工具名: {参数}}`
- `obj`: 包含对应方法的对象实例

**返回**：执行结果列表；异常也会被收集到结果中（因使用 `return_exceptions=True`）。

## 注意事项

- 同步函数会被投递到线程池中执行。
- 建议配合 `aioverse.Typing` 中的类型注解生成工具描述。
