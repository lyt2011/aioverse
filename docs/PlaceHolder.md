# PlaceHolder 模块

提供空函数与空对象，用于默认值注入或接口占位。

## 空函数

```python
from aioverse.PlaceHolder import asyncNull, syncNull

await asyncNull()   # 什么都不做
syncNull()          # 什么都不做
```

## NullObject

一个特殊的空对象：可 await、可调用、可访问任意属性，始终返回自身。

```python
from aioverse.PlaceHolder import NullObject

null = NullObject()

# 以下操作均安全且返回 null 自身
null.foo().bar()
await null.async_method()
null.any_attribute
```

**适用场景**：
- 作为可选日志、缓存等组件的默认注入值，避免满屏 `if x is not None` 判断。
- 需要静默忽略某些调用时的占位符。
