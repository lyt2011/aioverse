# LogProtocol

日志协议抽象基类。

## 抽象方法

```python
class MyLogger(LogProtocol):
    def log(self, text: str) -> None:
        ...
```

定义了最基础的日志记录接口。
