# OpenAI 模块

提供 OpenAI Chat Completions API 的异步封装，包含全局会话管理、客户端请求与安全请求函数。

## 全局会话管理

| 函数 | 说明 |
|------|------|
| `createSession()` | 创建全局 `aiohttp.ClientSession` |
| `getSession()` | 获取当前全局会话 |
| `asyncCloseSession()` | 异步关闭全局会话 |
| `syncCloseSession()` | 同步关闭全局会话（不保证在所有环境可用） |

## OpenAIClient

继承 `OpenAIProtocol`，封装聊天补全请求。

### 构造函数

```python
client = OpenAIClient(
    model: str,                        # 模型名称
    api_url: str,                      # API 端点
    asyncLog: LogProtocol = None,      # 日志实例（可选）
    keyManager: KeyManager = None,     # 密钥管理器（可选）
    session: ClientSession = None      # 自定义会话（可选）
)
```

### chatCompletion

```python
item = await client.chatCompletion(
    contextManager: ContextManager,    # 上下文管理器
    headers: dict = {},                # 额外请求头
    params: dict = {},                 # URL 参数
    body: dict = {},                   # 额外请求体
    timeout: int = 90                  # 超时时间（秒）
)
```

**返回**：`Item` 对象，包含以下属性：
- `model` - 实际使用的模型
- `request_id` - 请求 ID
- `content` - AI 回复正文
- `reasoning` - 推理内容（如有）
- `token` - 嵌套 `Item`，含 `prompt`, `completion`, `total`, `cached`

**异常**：`ResponseCodeError` - 当 HTTP 状态码非 200 时抛出。

### setKeyManager

运行时更换密钥管理器。

```python
client.setKeyManager(new_key_manager)
```

## safeRequest

带自动重试与异常处理的安全请求函数。

```python
result = await safeRequest(
    openAIClient: OpenAIProtocol,
    contextManager: ContextManager,
    exceptionHandler = None,    # 异常处理器
    maxRetryCount: int = 3,     # 最大重试次数
    **kwargs                    # 透传给 chatCompletion
)
```

**返回**：成功时返回 `Item`；失败时返回 `Error` 对象。

**重试逻辑**：
- 当异常处理器返回 `RETRY` 且未超过最大重试次数时递归重试。
- 返回 `ABORT` 或超过重试次数时返回 `Error`。

## 使用示例

```python
from aioverse.OpenAI import createSession, OpenAIClient, safeRequest
from aioverse.managers import ContextManager, KeyManager
from aioverse.types import Context, Prompt

createSession()

client = OpenAIClient(
    model="gpt-3.5-turbo",
    api_url="https://api.openai.com/v1/chat/completions",
    keyManager=KeyManager(["sk-xxx"])
)

cm = ContextManager()
cm.setPrompt(Prompt(content="请用中文回答"))
cm.addContext(Context(role="user", content="讲个笑话"))

result = await safeRequest(client, cm)
if hasattr(result, "content"):
    print(result.content)
```
