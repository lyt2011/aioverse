# LogWriteProtocol

日志写入协议抽象基类。

## 抽象方法

```python
class MyWriter(LogWriteProtocol):
    def write(self, text: str, flush: bool = False) -> None:
        ...
```

- `text`：待写入的日志内容。
- `flush`：为 `True` 时强制刷盘/输出。
