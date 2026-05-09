# JsonManager

基于内置 `dict` 的 JSON 管理器，提供链式加载与便捷访问。

## 构造函数

```python
from aioverse.managers import JsonManager

jm = JsonManager()
```

## 方法

| 方法 | 说明 |
|------|------|
| `fromDict(dictionary)` | 从字典加载 |
| `fromString(string)` | 从 JSON 字符串加载（使用 `orjson`） |
| `fromFile(path)` | 从文件加载 |
| `toDict()` | 返回自身字典 |
| `toString()` | 转为 JSON 字符串 |
| `hasKey(key)` | 是否包含某键 |
| `setValue(key, value)` | 设置键值 |
| `getValue(key, default)` | 安全取值 |
| `delValue(key)` | 删除键 |

## 使用示例

```python
jm = JsonManager()
jm.fromFile("config.json")

if jm.hasKey("api_url"):
    print(jm.getValue("api_url"))

jm.setValue("debug", True)
```

> 注意：不做异常捕获，所有解析错误均向上抛出。
