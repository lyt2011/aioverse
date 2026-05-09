# LogFormatProtocol

日志格式化协议抽象基类。

## 抽象方法

```python
class MyFormatter(LogFormatProtocol):
    def format(self, text: str, level: str) -> str:
        ...
```

负责将日志文本与级别转换为最终输出字符串。
