# Hack Girlfriend

## 隐私说明
涉及聊天记录、账号密码等隐私信息的文件，请以'sec.txt'为后缀名。


## 项目目录结构说明
### Applications
单个应用以flask-blueprint来做，在Applications里做路由转发。

### Platform
Applications转发到此（有一个对应关系）。

### Docs
项目中用到的技术，学习中可以留下**简要**的文档。

### Libraries
项目中用到的库（第三方或者自建）。

### PackageData
公用配置信息。（暂时还没太想好）

### Spider
项目中用到的爬虫。

## TODO LIST

- [ ] QQ Bot
    - 模块化： 进行中
    - 群聊监听保存聊天记录
    - 私聊机器人（图灵+其他）
- [ ] QQ Records Analysis
    - 対txt的私聊记录进行**时间、话题、情感**分析。
    - 对群聊记录进行分析
    - 自动化获取聊天记录
- [ ] 语音合成
    - [ ] 接入百度语音REST API
    - 接入讯飞API，需要做其他语言到python的桥接，待定
    - fmod api的python接口实现，难度较大，不如直接在其他平台原生实现。
    

# Refs




