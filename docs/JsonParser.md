# JsonParser 模块

深度 JSON 解析器，自动递归解析嵌套的 JSON 字符串或 Python 字面量。

## deepJsonParser

```python
from aioverse.JsonParser import deepJsonParser

# 单层 JSON
data = deepJsonParser('{"key": "value"}')

# 嵌套 JSON（多层转义）
nested = deepJsonParser('{"outer": "{\"inner\": 1}"}')
# 结果: {"outer": {"inner": 1}}

# 列表递归
arr = deepJsonParser('["{\"a\": 1}", "normal"]')
# 结果: [{"a": 1}, "normal"]
```

**解析策略**：
1. 对字符串尝试 `orjson.loads` 进行 JSON 解析。
2. 失败则回退到 `ast.literal_eval` 解析 Python 字面量。
3. 均失败则保留原字符串。
4. 对字典与列表递归处理所有元素。

**返回**：解析后的 Python 对象（字典、列表、基础类型等）。
