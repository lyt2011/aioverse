# OpenAIProtocol

OpenAI 客户端抽象基类，定义了聊天补全协议接口。

## 抽象方法

```python
class MyClient(OpenAIProtocol):
    async def chatCompletion(
        self,
        headers: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None,
        timeout: int = 90
    ) -> str | Dict[str, Any]:
        ...
```

任何自定义 OpenAI 客户端均应继承此协议并实现 `chatCompletion` 方法。
