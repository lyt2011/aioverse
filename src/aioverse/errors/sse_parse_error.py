from __future__ import annotations


class SSEParseError(Exception):
    """连续的 SSE data 事件无法解码为响应块。

    抛出前可能已经 yield 过有效 chunk，因此调用方重试请求时需要自行避免重复输出。
    """

    ...
