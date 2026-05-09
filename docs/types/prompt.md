# Prompt

系统提示词，继承自 `Context`，固定 `role="system"`。

## 构造函数

```python
from aioverse.types import Prompt

prompt = Prompt(content="你是一个 Python 专家")
```

等效于：

```python
Context(role="system", content="你是一个 Python 专家")
```
