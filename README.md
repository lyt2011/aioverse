# 0.3.2更新日志

## Log.py (优化`get_log`方法逻辑)
1. 添加内部变量`_global_logs`，用于存储日志实例
2. `get_log`方法传入**完全相同**的参数时
  - `_global_logs`存在相同参数的键->**直接返回**对应日志实例
  - 不存在则**创建**并**记录**

## OpenAI.py
1. 删除`safeRequest`方法
2. `OpenAIClient.chatCompletion`的参数`contextManager`改名为`context_manager`

## 新增
1. 为`Content`新增`from_dict`方法，可以通过符合以下格式的字典转为实例
```python伪代码
{
	"type": <类型>,
	<类型>: <数据>
}
```
2. 为`Context`新增`from_dict`方法，可以将符合以下格式的字典转为Context实例 (`content`的值将被直接传入`Context`实例化，无论是`list`/`str`/`dict`/...)
```python伪代码
{
	"role": <角色>,
	"content": <内容>
}
```
3. 新增`utils/`文件夹，用于存放辅助工具
4. 新增`utils/syntax_sugar.py`，语法糖函数
5. `utils/syntax_sugar.py`新增`build_contexts`函数，用于将OpenAI标准上下文格式转为ContextManager
6. `aioverse.types.context`新增`to_raw_dict`方法，返回带有`token`, `content`, `role`完整信息的字典

## Future
1. 将更多使用驼峰命名的函数名/参数改为蛇形命名 (写java写傻了)
2. 可能会支持流式输出，等我去研究研究OpenAI流式输出格式先😋😋

# 0.3.1更新日志

## Log.py
1. `getLog`函数改名为`get_log`
2. `asyncWriter`与`syncWriter`添加`flush`参数，默认值`False`，当传入`True`时 强行写入缓冲区内容
```python
flush: bool = False
```

## OpenAI.py
1. `OpenAIClient`的`apiUrl`改名为`api_url`

# 0.3.0更新日志

## OpenAI.py的OpenAIClient类
1. 返回类型由`str`改为`Item`，添加了**可扩展性**
2. 支持返回`token`, `model`, `request_id`, `reasoning`
  - `token`: token使用量
  - `model`: 使用的模型
  - `request_id`: 请求id
  - `reasoning`: 思维链
3. 优化请求参数构建逻辑，`headers`, `params`, `body`均采用`**`解包

## managers.ContextManager
1. 属性`self._context`更名为`self._contexts`
2. 添加`_token`属性
  - 可在实例化时通过`token`可选参数传入
  ```python
  ContextManager(token=114514)
  ```
  - 也可以在实例化后通过实例的`setToken`方法传入
  ```python
  ContextManager().setToken(114514)
  ```
3. 新增使用装饰器`property`的`token`方法
  1. 当`self._token`小于等于`0`->通过遍历`self._contexts`并相加后*1.3
  2. 当`self._token`大于`0`->直接返回`self._token`
4. `isOut()`方法更改
  - 参数`maxToken`改名为`max_token`
  - 使用`self.token`函数来获取token用量
5. `clear()`方法更新
  - 添加`keep_prompt`(`bool`)参数，可选是否保留上下文

# 0.2.4更新日志
- 为`Context`类添加了一个`token`参数
  - 默认值为`None`
  - 当值不为默认值时->`len(Context)`返回的是`self.token`的值
  - 当值为默认值时->`len(Context)`返回`self.content`的`__len__`方法返回值
  - 这是为了后续自定义上下文占用token预留了**接口**，增加**灵活性**

# 0.2.3更新日志

## Item优化
1. 增加` __slots__ `属性，优化性能占用
2. ` __getattr__ `与` __setattr__ `使用`self._mapping`字典代理
3. `toDict()`返回一个**浅复制**的字典
4. `toDict()`与`toString()`支持动态属性

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