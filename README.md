# 0.4.0更新日志

## 新增

1. 新增 `models.tool_schema` 模块，包含 `Argument`、`Parameters`、`Function`、`Tool` 等 Pydantic 数据模型，用于定义 AI 可调用的工具结构
2. 新增 `models.tool_call_response` 模块，包含 `Function`、`ToolCall` 等 Pydantic 数据模型，用于处理 AI 返回的工具调用请求
3. 新增 `models.contexts.AssistantToolCalls`，专门处理 AI 返回的工具调用上下文（原 `ToolCalls` 改名）
4. 新增 `models.contexts.ToolExecuteResult`，用于构建工具执行结果上下文，支持 `tool_call_id` 关联
5. 新增 `managers.tool_manager.ToolManager`，提供工具注册、执行、序列化一体化管理
   - `register(func, tool)`：自动通过函数名注册工具
   - `tool_executer(tool_calls)`：安全执行工具调用，同步/异步函数自动适配，错误捕获并返回字符串
   - `to_list()`：导出为 OpenAI 标准 tools 格式
6. 新增 `utils.syntax_sugar.build_contexts`，支持将 OpenAI 格式的字典列表快速转为 `ContextManager`
7. 所有 Pydantic 模型新增 `to_dict()` 方法，统一序列化出口
8. 新增`models.ModelConfig`，用于配置模型，后续可能扩展`max_token`之类的可选参数

## 更改

1. `models.tool` 重命名为 `models.tool_schema`，语义更清晰（定义工具结构 vs 处理工具调用）
2. `models.tool_call` 重命名为 `models.tool_call_response`，语义更清晰（AI 返回的调用请求）
3. `models.contexts.ToolCalls` 重命名为 `AssistantToolCalls`，避免与 `tool_call_response` 模块混淆
4. `managers.context_manager` 修复方法名大小写：`hasPrompt()` → `has_prompt()`
5. `OpenAIClient.set_key_manager` 修复变量名：`keyManager` → `key_manager`
6. `models.contents.Segment.__len__` 修复变量名：`len(data)` → `len(self.data)`
7. `models.contexts.Context.to_dict` 修复循环变量判断：`isinstance(self.content, Segment)` → `isinstance(content, Segment)`
8. `models.contexts.AssistantToolCalls.to_dict` 修复未定义变量：`tool_calls` → `self.tool_calls`
9. `models.tool_schema.Parameters.to_dict` 修复字典遍历：`for name, arg in self.properties` → `for name, arg in self.properties.items()`
10. `utils.syntax_sugar.build_contexts` 修复不存在的类方法：`Context.from_dict()` → `Context(**context)`
11. `managers.tool_manager` 补充缺失的类型导入：`List`、`Any`
12. `OpenAIClient`的初始化传参的显式传入`api_url`等，更改为传入`models.ModelConfig`，便于扩展
13. `aioverse.types`的大部分类均基于pydantic重构并移动到`aioverse.models`里

## 删除

1. 删除 `models.tool_call.ToolCallsArray` 类，功能由 `List[ToolCall]` 直接替代，简化接口
