# 0.2.2更新日志
1. 为一些实例添加了` __slots__ `属性，**优化内存使用**
2. 将`ContentArray`的`addContent'`方法独立出2个方法
  - `addContent`: 仅支持使用`Content`实例添加
  - `addData`: **自动**通过传入参数构建`Content`对象，通过调用`addContent`方法添加

# 0.2.1更新日志
- 让`types.content_array.ContentArray.addContent`支持使用`types.content.Content`作为参数传入
  - 具体可查看`aioverse/types/content_array.py`

# 0.2.0更新日志

## **兼容多模态**
- 添加`Content`, `ContentArray`等抽象类以支持多模态
  - 目前关系`Content`->`ContentArray`->`Context`->`ContextManager`
- **`Content` 更新**
  - `upload_type`: 上传的类型
  - `upload_data`: 上传的数据
- **`ContentArray` 更新**
  - 可**链式调用**添加`Content`
  - toList() 方法输出类似
  ```json
  [
    {"type": "text", "text": "请描述这张图片"},
    {"type": "image_url", "image_url": "xxx.com/picture.png"}
  ]
  ```
- **`Context` 更新**
  - 支持`ContentArray`与`str`**混合使用**
- **`ContextManager` 修复**
  - 修复一些token统计的bug

- 为`Content`, `ContentArray`, `Context`均**添加了` __len__ `**，便于**token统计**

## 更改**文件关系**
  1. 原`model/`被**弃用**
  2. **结构体**分类为`types/`
  3. **错误**分类为`errors/`
  4. **协议**分类为`protocols/`

## 协议弃用
- `KeyManagerProtocol`, `ContextManagerProtocol`等协议被弃用
  - 纯占空间**作用不大**
  - 简单的类**无需**继承协议
  - 所有依赖`KeyManagerProtocol`与`ContextManagerProtocol`的脚本
    - `KeyManagerProtocol`**替换**为`KeyManager`
    - `ContextManagerProtocol`**替换**为`ContextManager`