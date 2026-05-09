# ContextManager

对话上下文管理器，维护 Prompt 与多轮对话历史，支持 Token 估算与自动裁剪。

## 构造函数

```python
from aioverse.managers import ContextManager
from aioverse.types import Context

cm = ContextManager(
    context_array=[Context(role="system", content="助手")],
    token=0     # 0 表示自动估算
)
```

## 核心方法

| 方法 | 说明 |
|------|------|
| `setPrompt(prompt)` | 设置/替换系统提示词 |
| `getPrompt()` | 获取当前提示词 |
| `hasPrompt()` | 是否已设置提示词 |
| `addContext(context)` | 添加一条对话 |
| `deleteLastContext()` | 删除最后一条对话 |
| `clear(keep_prompt=False)` | 清空上下文；`True` 时保留提示词 |
| `toList(return_prompt=True)` | 转为 OpenAI 消息列表 |
| `isOut(max_tokens)` | 当前 token 是否超出限制 |
| `trim()` | 删除最旧的一条上下文（保留提示词时删第 2 条） |
| `setToken(token)` | 设置自定义 token 数 |

## Token 估算

当 `token <= 0` 时，自动按 `总字符数 * 1.3` 估算。

## 使用示例

```python
from aioverse.managers import ContextManager
from aioverse.types import Prompt, Context

cm = ContextManager()
cm.setPrompt(Prompt(content="你是翻译官"))
cm.addContext(Context(role="user", content="Hello"))
cm.addContext(Context(role="assistant", content="你好"))

if cm.isOut(4096):
    cm.trim()

messages = cm.toList()
```
