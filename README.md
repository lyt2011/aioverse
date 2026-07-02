# aioverse

[![Python Version](https://img.shields.io/badge/python-%3E%3D3.11-blue)](https://www.python.org/)
[![Version](https://img.shields.io/badge/version-0.4.1-green)]()

基于 `aiohttp` 构建的轻量异步 OpenAI API 请求库。内置**上下文管理**、**工具调用 (Function Calling)**、**多密钥轮询**与**多模态内容**支持。所有数据模型基于 `Pydantic v2`，开箱即用。

> 设计哲学：**轻量、专注核心、拒绝过度封装**

---

## ✨ 特性

- **纯异步** — 基于 `aiohttp` + `asyncio`，高并发无压力
- **工具调用** — 原生支持 Function Calling，工具 Schema 构建语法糖
- **上下文管理** — 对话历史组织、System Prompt 管理、Token 追踪与裁剪
- **密钥轮询** — `KeyManager` 多 Key 自动轮询，避免单点限流
- **多模态** — 内置 `Segment` 体系：文本、图片 URL、音频输入
- **Pydantic 全栈** — 请求参数、上下文、Schema、响应体全部带类型校验
- **可扩展日志** — 基于协议接口，支持自定义 Formatter 与 Writer，同步/异步双模式
- **空对象模式** — `NullObject` 安全吞掉任何调用，优雅处理可选依赖
- **全链路类型注解** — IDE 补全体验拉满

---

## 📦 安装

```bash
pip install aioverse
```

### 依赖

| 包名 | 版本 |
|------|------|
| Python | >= 3.11 |
| aiohttp | >= 3.11 |
| aiofiles | 25.1.0 |
| orjson | 3.11.9 |
| pydantic | 2.13.4 |

---

## 🚀 快速开始

### 基础对话

```python
import aiohttp
import asyncio
from aioverse import OpenAI
from aioverse.base_models import ModelConfig
from aioverse.base_models.contexts import Prompt, Context
from aioverse.managers import ContextManager

async def main():
    config = ModelConfig(
        model_name="gpt-4o",
        api_url="https://api.openai.com/v1/chat/completions",
        model_keys=["sk-your-key"],
    )

    async with aiohttp.ClientSession() as session:
        client = OpenAI.OpenAIClient(config, session)

        ctx = ContextManager()
        ctx.set_prompt(Prompt(content="你是一个乐于助人的助手。"))
        ctx.add_context(Context(role="user", content="你好，请介绍自己。"))

        response = await client.call(ctx)
        print(response.choices[0].message.content)

asyncio.run(main())
```

### 多密钥自动轮询

```python
config = ModelConfig(
    model_name="gpt-4o",
    api_url="https://api.openai.com/v1/chat/completions",
    model_keys=["sk-key-1", "sk-key-2", "sk-key-3"],
)
# KeyManager 自动管理轮询，失败自动切下一个
```

### 工具调用 (Function Calling)

```python
from aioverse.utils.syntax_sugar import build_tool_schema

# 构建工具 Schema
weather_tool = build_tool_schema(
    tool_name="get_weather",
    tool_description="获取指定城市的当前天气",
    requirements=["location"],
    arguments={
        "location": ("string", "城市名称，如：北京"),
    }
)

# 发送请求（注入工具）
response = await client.call(
    ctx,
    body={"tools": [weather_tool.model_dump()]}
)

# 处理工具调用
if response.choices[0].finish_reason == "tool_calls":
    ctx.add_context(response.choices[0].message)

    for call in response.choices[0].message.tool_calls:
        import json, asyncio
        args = json.loads(call.function.arguments)
        result = await get_weather(**args)

        ctx.add_context(type("ToolOutput", (), {
            "role": "tool",
            "tool_call_id": call.id,
            "content": result
        })())

    # 再次请求获取总结
    final = await client.call(ctx)
    print(final.choices[0].message.content)
```

### 多模态内容

```python
from aioverse.base_models.segments import Text, ImageUrl

# 文本 + 图片混合消息
context = Context(role="user", content=[
    Text(data="这张图里有什么？"),
    ImageUrl(data="https://example.com/image.jpg"),
])
```

---

## 📚 API 参考

### OpenAIClient

```python
class OpenAIClient:
    def __init__(
        self,
        model_config: ModelConfig,
        session: aiohttp.ClientSession,
        async_log: Optional[LogProtocol] = None
    ): ...

    async def call(
        self,
        context_manager: ContextManager,
        headers: Dict[str, Any] = {},
        params: Dict[str, Any] = {},
        body: Dict[str, Any] = {},
        timeout: int = 90,
    ) -> Response: ...
```

- `context_manager` — 对话上下文，通过 `to_list()` 导出为 messages 格式
- `headers` / `params` / `body` — 透传给 `session.post`，可用于注入 `tools`、`temperature` 等参数
- `timeout` — 请求超时时间（秒），默认 90s
- 返回 `Response` 模型（Pydantic），包含 `choices`、`usage`、`id` 等

### ContextManager

对话上下文组织器。内部通过 `_ContextsStatus` 维护状态。使用 `__slots__` 优化内存占用。

支持三种上下文块：

| 上下文块 | 说明 |
|---------|------|
| `Context` | 普通消息（user / assistant） |
| `ToolCallingBlock` | 工具调用块，包含请求与执行结果 |
| `ContextsBlock` | 普通消息块，可包含多条连续 Context |

```python
ctx = ContextManager()

# System Prompt
ctx.set_prompt(Prompt(content="你是..."))

# 添加用户消息
ctx.add_context(Context(role="user", content="你好"))

# 添加模型返回的工具调用
ctx.add_context(ToolCallingsContext(tool_calls=[...]))

# 添加工具执行结果
ctx.add_context(ToolOutput(content="结果", tool_call_id="call_xxx"))

# 导出为 OpenAI messages 格式
messages = ctx.to_list()     # -> List[Dict]

# 裁剪最早的一条上下文
ctx.trim()

# 清空（可选保留 Prompt）
ctx.clear(keep_prompt=True)

# Token 管理
ctx.set_token(114514)
print(ctx.token)
```

> ⚠️ `ContextsBlock` 和 `ToolCallingBlock` 均实现了 `ContextsBlockProtocol`，支持 `__iter__` / `append` / `insert` / `delete` 操作。

### KeyManager

多密钥轮询管理器。自动索引轮转，无可用密钥时抛出 `RuntimeError`。

```python
km = KeyManager(["sk-1", "sk-2"])

km.get_available_key()  # 获取当前或下一个可用 Key
km.get_current_key()    # 获取当前正在使用的 Key
km.get_next_key()       # 强制切换到下一个 Key
km.add_key("sk-3")
km.remove_key("sk-1")
```

### ModelConfig

模型配置定义。`model_alias` 不传则自动使用 `model_name`。

```python
class ModelConfig(BaseModel):
    model_name : str           # 模型名
    model_alias: str           # 别名（默认 = model_name）
    api_url    : str           # API 地址
    model_keys : List[str]     # 至少 1 个 Key

    max_token  : int = 0       # 最大生成长度
    token_limit: int = 0       # Token 上限（用于压缩判断）

    support_image: bool = False
    support_video: bool = False
    support_audio: bool = False
    support_tool : bool = False
    support_think: bool = False
```

### 工具 Schema 构建

两种方式构建 Tool Schema：

#### 方式一：语法糖（推荐）

```python
from aioverse.utils.syntax_sugar import build_tool_schema, _Empty

tool = build_tool_schema(
    tool_name="calculator",
    tool_description="简单的加减乘除计算器",
    requirements=["a", "b", "op"],
    arguments={
        "a": ("number", "第一个数字"),
        "b": ("number", "第二个数字"),
        "op": ("string", "运算符：+ - * /", "+"),  # 可选默认值
    }
)
```

#### 方式二：原生 Pydantic 模型

```python
from aioverse.base_models.tool_schema import Tool, Function, Parameters, Argument, _Empty

tool = Tool(
    function=Function(
        name="calculator",
        description="...",
        parameters=Parameters(
            properties={
                "a": Argument(type="number", description="第一个数字"),
                "b": Argument(type="number", description="第二个数字"),
            },
            required=["a", "b"]
        )
    )
)
```

> 还有野路子 `build_tool_schema_by_doc(func)`，通过解析函数注释中的 JSON 自动构建 Schema，仅供娱乐 😋

---

## 🧩 扩展机制

### 日志系统

基于协议接口设计，支持自定义实现：

| 协议 | 说明 |
|------|------|
| `LogProtocol` | 日志核心接口，包含 `log(text, level, flush)` 方法 |
| `LogFormatProtocol` | 格式化接口，负责日志文本与颜色格式化 |
| `LogWriteProtocol` | 写入接口，负责带缓冲区的文件写入 |

内置实现：

| 类 | 说明 |
|----|------|
| `AsyncLog` | 异步日志，`log()` 为 async 方法 |
| `SyncLog` | 同步日志，`log()` 为普通方法 |
| `AsyncWriter` | 异步文件写入，支持缓冲区批量 flush |
| `SyncWriter` | 同步文件写入，支持缓冲区批量 flush |
| `LogFormatter` | 默认格式化器，支持颜色分级（info/warn/error/debug/successful） |

```python
from aioverse.Log import get_log

# 获取日志实例（全局单例）
log = get_log("app.log", "myapp", is_async=True)
await log.log("服务启动成功", "successful")
await log.log("发生错误", "error", flush=True)
```

### 上下文块协议 (ContextsBlockProtocol)

所有上下文块（`ToolCallingBlock`、`ContextsBlock`）均实现该协议：

```python
class ContextsBlockProtocol(ABC):
    def __iter__(self) -> Iterator[Context]: ...
    def __len__(self) -> int: ...
    def append(self, context: Context): ...
    def insert(self, index: int, context: Context): ...
    def delete(self, index: int): ...
```

---

## 🛠️ 工具函数

### NullObject — 安全空对象

无论你怎么调用它，它都会安静地返回自身，绝不报错：

```python
from aioverse.utils.holder import NullObject

nope = NullObject()
nope()                          # -> NullObject
nope.log("hello")               # -> NullObject
await nope                      # -> NullObject
await nope.some_method(1, 2, 3) # -> NullObject
```

常用于可选依赖注入的默认值，优雅替代 `if xxx is not None` 检查。

---

## ❌ 错误处理

| 异常 | 说明 |
|------|------|
| `ResponseCodeError` | API 返回非 200 状态码时抛出，包含 `code` 和 `response` 属性 |

```python
from aioverse.errors import ResponseCodeError

try:
    response = await client.call(ctx)
except ResponseCodeError as e:
    print(f"API 错误: {e.code} - {e.response}")
```

---

## 📋 数据模型一览

| 模块 | 模型 | 说明 |
|------|------|------|
| `base_models.contexts` | `Context`, `Prompt`, `User`, `ToolCallingContext`, `ToolOutput` | 对话上下文 |
| `base_models.segments` | `Segment`, `Text`, `ImageUrl`, `AudioInput` | 多模态内容片段 |
| `base_models.model_config` | `ModelConfig` | 模型配置 |
| `base_models.tool_schema` | `Tool`, `Function`, `Parameters`, `Argument` | 工具定义 Schema |
| `base_models.tool_calling` | `ToolCalling`, `Function` | AI 返回的工具调用 |
| `models.blocks` | `ToolCallingBlock`, `ContextsBlock` | 上下文块 |
| `models.response` | `Response`, `Choice`, `Usage` | API 响应体 |
| `models._contexts_status` | `_ContextsStatus` | ContextManager 内部状态 |

---

## 🔄 更新日志

详见 [CHANGELOG.md](./CHANGELOG.md)

---

## 📄 许可证

MIT License
