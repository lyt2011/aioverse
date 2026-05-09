# KeyManager

轮询式 API 密钥管理器，支持多 key 自动轮换。

## 构造函数

```python
from aioverse.managers import KeyManager

km = KeyManager(["sk-key1", "sk-key2", "sk-key3"])
```

## 方法

| 方法 | 说明 |
|------|------|
| `getNextKey()` | 获取下一个密钥；无可用时抛 `RuntimeError` |
| `getCurrentKey()` | 获取当前正在使用的密钥 |
| `getAvailableKey()` | 获取当前密钥，若无则获取下一个 |
| `addKey(key)` | 追加密钥 |
| `removeKey(key)` | 删除指定密钥 |
| `__len__()` | 剩余密钥总数 |
| `__str__()` | 所有密钥拼接字符串 |

## 使用示例

```python
km = KeyManager(["key-A", "key-B"])
print(len(km))              # 2

key1 = km.getAvailableKey()  # key-A
key2 = km.getAvailableKey()  # 仍返回 key-A（当前密钥）
key3 = km.getNextKey()       # key-B
```
