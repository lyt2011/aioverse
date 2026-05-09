# ContentArray

管理 `Content` 实例的数组，支持验证、链式添加与状态查询。

## 构造函数

```python
from aioverse.types import ContentArray, Content

arr = ContentArray([Content("text", "Hello")])
```

## from_list

从字典列表创建实例，会自动验证格式。

```python
arr = ContentArray.from_list([
    {"type": "text", "text": "你好"},
    {"type": "image_url", "image_url": "http://example.com/1.jpg"}
])
```

**验证规则**：每个元素必须恰好包含 `type` 与对应类型键；仅支持 `text` 与 `image_url`。

## 链式操作

```python
arr.addContent(Content("text", "追加文本"))
arr.addData("image_url", "http://example.com/2.jpg")
```

## 属性与方法

| 名称 | 说明 |
|------|------|
| `toList()` | 转为字典列表 |
| `status` | 返回 `Item`，含 `is_pass`, `has_text`, `has_image` 等验证信息 |
| `__len__()` | 计算所有内容字符总数 |
| `__bool__()` | 判断是否包含内容 |
