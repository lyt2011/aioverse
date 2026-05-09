# SearchAI 模块

基于 [Tavily](https://tavily.com/) 的异步联网搜索封装。

## TavilyClient

### 构造函数

```python
client = TavilyClient(
    keyManager: KeyManager,      # 密钥管理器
    asyncLog: LogProtocol         # 日志实例
)
```

### search

```python
results = await client.search(
    query: str,          # 搜索关键词
    **kwargs             # 覆盖默认参数
)
```

**默认参数**：
- `include_answer`: `False`
- `include_images`: `False`
- `max_results`: `10`
- `timeout`: `15`

**返回**：搜索结果列表（`results` 字段）。

## 使用示例

```python
from aioverse.SearchAI import TavilyClient
from aioverse.managers import KeyManager
from aioverse.PlaceHolder import NullObject

km = KeyManager(["tvly-xxx"])
client = TavilyClient(km, NullObject())

results = await client.search("Python asyncio 教程", max_results=5)
for r in results:
    print(r.get("title"), r.get("url"))
```
