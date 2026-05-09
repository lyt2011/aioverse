# Item

动态属性容器，用于在函数间灵活传递数据。

## 构造函数

```python
from aioverse.types import Item

item = Item(
    default=None,       # 访问不存在的属性时返回的默认值
    name="test",
    value=123
)
```

## 特性

```python
print(item.name)        # "test"
print(item.unknown)     # None (default)

item.new_attr = "xxx"   # 动态添加属性
print(item.new_attr)    # "xxx"

# 序列化
item.toDict()           # {"name": "test", "value": 123, "new_attr": "xxx"}
item.toString()         # JSON 字符串
```

> 注意：`_mapping` 与 `_default` 受保护，不可直接修改 `_mapping`。
