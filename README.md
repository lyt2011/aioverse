# aioverse

[![Python Version](https://img.shields.io/badge/python-%3E%3D3.11-blue)](https://www.python.org/)
[![Version](https://img.shields.io/badge/version-0.4.6-green)](CHANGELOG.md)

基于 `aiohttp` 构建的轻量异步 OpenAI 兼容 API 请求库。它提供 `Request` 请求构建器、Pydantic 上下文与响应模型、SSE 流式解析，以及文本、图片、音频和视频内容段。

> 设计哲学：轻量、专注核心、拒绝过度封装。

## 特性

- 纯异步：基于 `aiohttp` 和 `asyncio`。
- 普通请求：`OpenAIClient.call()` 返回经过 Pydantic 校验的 `Response`。
- 流式请求：`call_stream()` 按 SSE 事件产出 `StreamChunk`。
- 请求构建：`Request` 支持 headers、params、body、完整请求超时和流式空闲超时。
- SSE 容错：支持跨传输分块 UTF-8、多行 `data:`、EOF、`[DONE]` 和连续解析失败阈值。
- 工具调用模型：用 `ToolCallingContext` 和 `ToolOutputContext` 表示模型调用与工具结果。
- 多模态：支持文本、图片、音频和视频 Segment。
- Pydantic 数据模型：请求上下文、响应体和流式增量均有明确类型。
- 标准日志：使用 Python 标准库 `logging`。
- 空对象：`NullObject` 可用于可选依赖的无操作占位。

`aioverse` 是底层请求库，不执行工具、不维护会话历史、不自动轮换密钥，也不隐式重试请求。多轮编排、工具执行、密钥切换和重试策略由上层应用负责。`NullObject` 的导入路径是 `from aioverse.holder import NullObject`。

## 安装

```bash
pip install /path/to/aioverse
```

运行时依赖：

| 包名 | 版本 |
|---|---|
| Python | `>=3.11` |
| aiohttp | `>=3.11` |
| aiofiles | `==25.1.0` |
| orjson | `==3.11.9` |
| pydantic | `==2.13.4` |

## 快速开始

### 普通请求

```python
import asyncio

import aiohttp

from aioverse.OpenAI import OpenAIClient
from aioverse.models import UserContext


async def main():
    async with aiohttp.ClientSession() as session:
        client = OpenAIClient(
            session,
            api_url="https://api.openai.com/v1/chat/completions",
            model_name="gpt-4o",
        )

        response = await client.call(
            context_list=[UserContext(content="你好，请介绍自己。")],
            assistant_key="Bearer sk-your-key",
        )
        print(response.choices[0].message.content)


asyncio.run(main())
```

`assistant_key` 会直接写入 `Authorization` 请求头。示例中的 `sk-your-key` 只是占位符，不要把真实密钥提交到代码仓库。

### 自定义 Request

`Request` 可用于显式构建请求头、参数和请求体：

```python
from aioverse.models import Request, UserContext

request = Request(
    url="https://api.openai.com/v1/chat/completions",
    timeout=120,
    stream_idle_timeout=30,
)
request.set_header("Authorization", "Bearer sk-your-key")
request.set_body("model", "gpt-4o")
request.set_body(
    "messages",
    [UserContext(content="你好").model_dump(mode="json")],
)

response = await client.call(request=request)
```

`Request.timeout` 默认 300 秒，覆盖 HTTP 请求的完整生命周期。`Request.stream_idle_timeout` 默认 60 秒，只限制等待下一个已解析流式块的时间；设为 `None` 可以关闭额外的流式 watchdog。

### 流式请求

```python
from contextlib import aclosing

from aioverse.models import Request

request = Request(
    url="https://api.openai.com/v1/chat/completions",
    stream_idle_timeout=30,
)
request.set_header("Authorization", "Bearer sk-your-key")
request.set_body("model", "gpt-4o")
request.set_body("messages", [{"role": "user", "content": "说一句问候"}])

async with aclosing(client.call_stream(request=request)) as stream:
    async for chunk in stream:
        if chunk.choices:
            delta = chunk.choices[0].delta
            print(delta.content or "", end="")
```

流式解析器会将多个 `data:` 行按 SSE 规则拼接，在遇到 `[DONE]` 后结束。传输层可以把一个 UTF-8 字符拆到多个网络分块中，增量解码器会保留未完成的字节。连续多个数据事件无法解析为 `StreamChunk` 时会抛出 `SSEParseError`，而不是无限吞掉错误。提前停止消费时请使用 `contextlib.aclosing`，确保 HTTP 响应及时释放。

### 工具调用请求

工具 Schema 和执行逻辑由调用方维护，`aioverse` 只负责发送和解析数据：

```python
import json

from aioverse.models import ToolCallingContext

weather_tool = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "获取指定城市的当前天气",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "城市名称"},
            },
            "required": ["location"],
        },
    },
}

request.set_body("tools", [weather_tool])
response = await client.call(request=request)

if response.choices[0].finish_reason == "tool_calls":
    message = ToolCallingContext.model_validate(
        response.choices[0].message.model_dump(mode="json")
    )
    tool_messages = []
    for call in message.tool_calls:
        args = json.loads(call.function.arguments)
        result = await get_weather(**args)
        tool_messages.append({
            "role": "tool",
            "content": result,
            "tool_call_id": call.id,
        })

    request.set_body("messages", [
        *request.body["messages"],
        message.model_dump(mode="json"),
        *tool_messages,
    ])
    final = await client.call(request=request)
    print(final.choices[0].message.content)
```

### 多模态内容

```python
from aioverse.models import (
    AudioInputSegment,
    AudioUrlSegment,
    TextSegment,
    UserContext,
    VideoInputSegment,
    VideoUrlSegment,
)

context = UserContext(content=[
    TextSegment(text="请分析这些媒体内容。"),
    AudioInputSegment(data="...", format="wav"),
    AudioUrlSegment(url="https://example.com/audio.mp3"),
    VideoInputSegment(data="...", format="mp4"),
    VideoUrlSegment(url="https://example.com/video.mp4"),
])
```

`AudioInputSegment` 和 `VideoInputSegment` 接收 Base64 数据；`AudioUrlSegment` 和 `VideoUrlSegment` 引用远程 URL。它们只描述请求内容，不负责读取、上传、下载、转码或抽帧。实际端点是否接受对应媒体类型由调用方和模型能力决定。

## API 参考

### `OpenAIClient`

```python
class OpenAIClient:
    def __init__(
        self,
        session: aiohttp.ClientSession,
        api_url: str | None = None,
        model_name: str | None = None,
    ): ...

    async def call(
        self,
        *,
        context_list: list[BaseContext] | None = None,
        assistant_key: str | None = None,
        request: Request | None = None,
    ) -> Response: ...

    async def call_stream(
        self,
        *,
        context_list: list[BaseContext] | None = None,
        assistant_key: str | None = None,
        request: Request | None = None,
    ) -> AsyncIterator[StreamChunk]: ...
```

- `context_list`：`BaseContext` 列表；通过便捷参数构建请求时，Pydantic 上下文会转换为 JSON。
- `assistant_key`：直接写入 `Authorization` 请求头的值。
- `request`：可复用的 `Request` 构建器；传入后调用方负责设置所需的 URL、headers 和 body。
- `call()`：发送非流式请求，HTTP 状态为 200 后继续校验 `Response` schema。
- `call_stream()`：发送流式请求，返回按 SSE 事件解析的 `StreamChunk` async generator。

### `Request`

```python
request = Request(url="https://example.com/v1/chat/completions")
request.set_header("Content-Type", "application/json")
request.set_param("trace", "1")
request.set_body("model", "gpt-4o")
```

`set_header()`、`set_param()` 和 `set_body()` 都返回当前 Request，便于链式构建。`headers`、`params` 和 `body` 属性用于读取将要交给 `aiohttp.ClientSession.post()` 的值。

### 上下文和响应模型

上下文模型包括 `BaseContext`、`SystemContext`、`UserContext`、`AssistantContext`、`ToolCallingContext` 和 `ToolOutputContext`。工具调用通过 `ToolCallingContext.tool_calls` 保存，工具结果通过 `ToolOutputContext.tool_call_id` 关联。

响应模型包括 `Response`、`Choice`、`Usage`、`StreamChunk`、`StreamChoice` 和 `Delta`。具体字段遵循 OpenAI Chat Completions 风格，并由 Pydantic 校验。

## 错误处理

| 异常 | 说明 |
|---|---|
| `ResponseCodeError` | API 返回非 200 状态码时抛出，包含 `code` 和 `response` 属性 |
| `SSEParseError` | 连续多个 `data` 事件无法解析为 `StreamChunk` 时抛出 |
| `asyncio.TimeoutError` | HTTP 请求超时或流式空闲超时 |

```python
from contextlib import aclosing

from aioverse.errors import ResponseCodeError, SSEParseError

try:
    async with aclosing(client.call_stream(request=request)) as stream:
        async for chunk in stream:
            if chunk.choices:
                print(chunk.choices[0].delta.content or "", end="")
except ResponseCodeError as error:
    print(f"API 错误: {error.code} - {error.response}")
except SSEParseError:
    print("流式响应格式损坏")
```

## 项目结构

```text
aioverse/
├── src/aioverse/
│   ├── OpenAI.py                 # OpenAI 兼容客户端和 SSE 解析器
│   ├── enums/                    # 请求角色枚举
│   ├── errors/                   # HTTP 和 SSE 错误
│   ├── holder.py                 # NullObject
│   ├── models/
│   │   ├── request.py            # Request 构建器
│   │   ├── contexts/             # 对话上下文
│   │   ├── segments/             # 图片、音频、视频等内容段
│   │   ├── response/             # 普通和流式响应模型
│   │   └── tool_calling/         # 工具调用响应模型
│   └── protocols/                # 日志等协议接口
├── tests/
├── pyproject.toml
├── README.md
└── CHANGELOG.md
```

## 开发与验证

在项目根目录执行：

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q src tests
git diff --check
```

测试覆盖多模态模型、SSE 分片解析、UTF-8 跨分块、EOF、`[DONE]`、解析错误阈值、空闲超时、错误响应和流式资源释放。

## 许可证

MIT License
