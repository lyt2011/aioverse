# Typing 模块

专为 AI Function Calling 设计的类型注解工具，可将类型转换为字符串描述，便于向大模型提供工具参数信息。

> **注意**：这些类型仅用于生成描述字符串，**不能**用于 `isinstance` 判断，也不被常规类型检查工具识别。

## 基础类型

| 类型 | 字符串表示 |
|------|-----------|
| `String` | `string` |
| `Int` | `int` |
| `Float` | `float` |
| `Bool` | `bool` |

## 复合类型

```python
from aioverse.Typing import List, Dict, Union, Optional

List["string"]                # "List[string]"
Dict[("string", "int")]       # "Dict[string: int]"
Union[("int", "string")]      # "Union[int or string]"
Optional["string"]            # "Union[string or None]"
```

## 使用示例

```python
from aioverse.Typing import String, Int, List
from aioverse.AITools import FunctionTools

def search(query: String, max_results: Int = 5) -> List["string"]:
    """搜索并返回结果列表"""
    ...

print(FunctionTools.functionToDict(search))
```
