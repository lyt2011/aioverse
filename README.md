# 0.2.0更新日志

## **兼容多模态**
- 添加`Content`, `ContentArray`等抽象类以支持多模态
  - 目前关系**`Content`**->**`ContentArray`**->**`Context`**->**`ContextManager`**
- **`Content`**
  - `upload_type`: 上传的类型
  - `upload_data`: 上传的数据
- **`ContentArray`**
  实现类似
  ```json
  [
    {"type": "text", "text": "请描述这张图片"},
    {"type": "image_url", "image_url": "xxx.com/picture.png"}
  ]
  ```
  的操作
- **`Context`**
  - 支持`ContentArray`与`str`**混合使用**
- **`ContextManager`**
  - 修复一些token统计的bug

- 为`Content`, `ContentArray`, `Context`均**添加了` __len__ `**，便于**token统计**

## 更改**文件关系**
  1. 原**`model`**被**弃用**
  2. 结构体分类为**`types`**
  3. 错误分类为**`errors`**
  4. 协议分类为**`protocols`**

## 协议弃用
1. **`KeyManagerProtocol`**, **`ContextManagerProtocol`**等协议被弃用
  - 纯占空间**作用不大**
  - 简单的类**无需**继承协议
  - 所有依赖**`KeyManagerProtocol`**与**`ContextManagerProtocol`**的脚本
    - **`KeyManagerProtocol`**替换为**`KeyManager`**
    - **`ContextManagerProtocol`**替换为**`ContextManager`**