# Python基础
## 基础数据类型、结构
- str
- int
- dict
- list
- tuple

## 核心/常用库
- json
- datetime
- requests

# 一些Tips
1. 判断字典有无某字段
>推荐`key in dict`，而不是`dict.has_key(key)`。
 
2. 获取、赋值字典未知字段
>`dict.get(key)`，`dict[key]=value`。

3. C语言的三元表达式等效
`a = b if b==True else False`