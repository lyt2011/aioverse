# Log 模块

提供异步与同步双模式的日志系统，支持彩色终端输出与文件缓冲写入。

## 核心组件

### LogFormatter

负责将日志格式化为带颜色与不带颜色两个版本。

```python
formatter = LogFormatter(source="MyApp")
no_color, color = formatter.format(text="启动", time="2024-01-01", level="info")
```

**支持的级别**：`info`, `warn`, `error`, `debug`, `successful`（不区分大小写）。

### AsyncWriter / SyncWriter

日志写入器，内置缓冲区（默认 `bufSize=10`），减少频繁 IO。

```python
writer = AsyncWriter(logFileName="app.log", bufSize=20)
await writer.write("一条日志", flush=False)   # 加入缓冲区
await writer.write("", flush=True)             # 强制刷盘
```

### AsyncLog / SyncLog

完整的日志类，继承 `BaseLog`，组合了 `Formatter` 与 `Writer`。

```python
log = AsyncLog(formatter=formatter, writer=async_writer)
await log.log("服务启动", level="info", flush=True)
```

### get_log

便捷工厂函数，一键创建日志实例。

```python
from aioverse.Log import get_log

logger = get_log("runtime.log", source="Bot", isAsync=True)
await logger.log("连接成功", "successful")
```

| 参数 | 说明 |
|------|------|
| `fileName` | 日志文件名 |
| `source` | 日志来源标识 |
| `isAsync` | `True` 创建 `AsyncLog`，否则创建 `SyncLog` |

## 使用示例

```python
from aioverse.Log import get_log
import asyncio

async def main():
    logger = get_log("bot.log", "ChatBot", isAsync=True)
    await logger.log("开始运行", "info")
    await logger.log("遇到警告", "warn")
    await logger.log("发生错误", "error", flush=True)

asyncio.run(main())
```
