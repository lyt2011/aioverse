# aioverse 使用文档

aioverse 是一个面向异步 AI 应用开发的 Python 工具库，提供 OpenAI API 封装、联网搜索、日志系统、上下文管理、密钥轮询等模块化能力。

## 目录结构

- **OpenAI** - OpenAI 异步客户端与请求封装
- **SearchAI** - Tavily 联网搜索客户端
- **Log** - 异步/同步日志系统
- **AITools** - AI 函数工具反射与并发执行
- **JsonParser** - 深度 JSON 解析器
- **ExceptionHandler** - API 异常处理策略
- **PlaceHolder** - 空对象与占位函数
- **Typing** - AI 友好的类型注解
- **types** - 核心数据类型（Context, Item, Content 等）
- **protocols** - 抽象协议接口
- **errors** - 异常定义
- **managers** - 管理器（上下文、密钥、JSON）
- **const** - 常量定义

## 快速开始

```python
import asyncio
from aioverse.OpenAI import createSession, OpenAIClient, safeRequest
from aioverse.managers import ContextManager, KeyManager
from aioverse.types import Prompt, Context

async def main():
    createSession()
    
    km = KeyManager(["your-api-key"])
    client = OpenAIClient(
        model="gpt-4",
        api_url="https://api.openai.com/v1/chat/completions",
        keyManager=km
    )
    
    cm = ContextManager()
    cm.setPrompt(Prompt(content="你是一个有用的助手"))
    cm.addContext(Context(role="user", content="你好"))
    
    result = await safeRequest(client, cm)
    print(result.content)

asyncio.run(main())
```

> 注意：全局会话需要手动创建，使用后建议调用 `asyncCloseSession()` 关闭。
