# 0.3.3更新日志

## 说明

1. 感觉原来的项目垃圾太多了，我的设计理念就是一个`简单`, `轻量`的openai请求库，所以给垃圾全删了，仅保留核心功能

## 新增

1. `aioverse.managers.ContextManager`新增`getList`方法，返回实例的`self._contexts`

## 更改

1. `aioverse.types.Context`的`content`不再强行绑定`ContentArray`，只要该实例支持`toString`或`toList`都行，兜底`str()`
2. `OpenAI.py`基本移除所有的驼峰命名，`OpenAIClient`的`chatCompletion`方法改名为`call`
3. 项目的所有驼峰命名基本已经转为蛇形命名
4. `ContentArray`模块迁移至`models/`内，用pydantic用于类型验证

## 移除

1. 移除`AITools`模块(没用，且需要提示词支持)
2. 移除`Typing.py`(`AITools`模块的依赖，跟着移除)
3. 移除`ExceptionHandler`模块，请自行解决错误处理(因为原本的就没有搞好 没法预料所有的错误)