# 你好，这里是HackGirlfriend！ 
If [English Prefered](https://cannot.cc/HackGirlfriend/README_EN) :shipit: :sunglasses:。

HackGirlfriend是我真正意义上的第一个GitHub开源项目，也是一个“系统”的Web服务器后台项目。**你可以访问 [api.cannot.cc](https://api.cannot.cc/) 来获取更多功能测试方面的信息。**

我计划将它打造为一个高可扩展性的后台，引入诸如QQ聊天机器人、NBA数据分析、学生组织后台管理等有趣或有着高频次需求的完全独立的、模块化的应用。性能也是追求之一。

由于我基本处于学习中的Web菜鸟阶段以及作为高年级的本科生，也身处技术学校的技术团队，HackGirlfriend将主要用于向高手学习、与网络探究、与同辈交流、指导学弟学妹。

起名是一件有学问的事情。不要把HackGirlfriend打错成 'HackGrilfriend' 或者 'HackGirlfirend'喔^_^（这是我经常干的事情，如果没有Tab自动完成的话）。

## HackGirlfriend是什么？
前文已提到作为“父母”的我所希望的HackGirlfriend是什么。由于项目仍在比较初级的v0.0.1阶段（已上线公网服务器以及较少的功能，但仍长期处于Debug状态），因此这个问题还是等它长大一点再回答吧。

>Google一下HackGirlfriend，这张图令我印象深刻！https://img.wonderhowto.com/img/87/03/63528600955598/0/hack-like-pro-hack-windows-7-see-whether-your-girlfriend-is-cheating-not.1280x600.jpg

## HackGirlfriend能做什么？

由于这是一项进展中的项目，而且要满足“高可扩展性”的验证，以及“有趣的”、“高频次需求的”这些指标，这个列表将会持续更新（注：按照各项的开始时间排序，完成部分功能即打钩)。

* [x] 文字转语音，基于百度语音的RESTful API，将文字转为声音文件。目前只完成api的简单转发。（一开始是想拿到百度的声音来做音频处理的，发现难度略大）[试一试](https://api.cannot.cc/speak/hello_world)

* [x] QQ聊天记录分析, 导出QQ聊天记录的txt文件，可得到聊天记录的时间、频次、内容、情感等自然语言处理分析记录。目前是本地运行的应用（暂不支持web端）。

* [x] QQ聊天机器人，支持Web端扫描二维码登录开启基于图灵API的聊天机器人，支持群聊以及私聊，并支持部分参数设置。[试一试](https://api.cannot.cc/qqbot/one)

* [x] 醉晚亭工作室部门管理后台，会议记录+请假系统+投票系统+成员管理。[试一试](https://api.cannot.cc/zuiwan/get-users-list) 

* [ ] Secret App 服务端。[Secret](https://github.com/Danceiny/Secret)是我的一个类似带朋友圈的私密聊天Android项目。

* [ ] NBA数据分析, 基于某项NBA+Programming主题的比赛获奖项目。

与HackGirlfriend强相关的还有本人的姊妹项目[HG-admin](https://github.com/Danceiny/HG-admin)，HackGirlfriend的后台管理系统前端。

# 如何部署HackGirlfriend到你的主机上？

有关部署平台的选择，我在开发中力求兼顾平台兼容性，基本功能在Linux/OS X/Windows上均能正常工作，当然也有平台相关的无能为力。详见[HackGirlfriend的平台兼容性](https://cannot.cc/HackGirlfriend/Platform)。

**首先，需要安装所有依赖。这些依赖有些是跑整个框架的必需依赖，也有些是非必需项、可替换项。详情**
See [Dependencies](https://cannot.cc/HackGirlfriend/Dependencies)。

**然后嗯，把HackGirlfriend搞到您的公网服务器上吧。**
See [DeployWebServer](https://github.com/Danceiny/HackGirlfriend/DeployWebServer)。
 
 or See [Docker Deploy](https://cannot.cc/HackGirlfriend/Docker).

# 相关原创文档列表

- [Flask初探以及在HackGirlfriend中的实战应用](https://cannot.cc/HackGirlfriend/Flask)
- [Flask + uWSGI + supervisor在Linux服务器上的部署](https://cannot.cc/HackGirlfriend/DeployWebServer)

- [Docker快速部署](https://cannot.cc/HackGirlfriend/Docker)
- [ThreadPool](https://cannot.cc/HackGirlfriend/ThreadPool)
- [Celery](https://cannot.cc/HackGirlfriend/Celery)

- [Python语言要点](https://cannot.cc/HackGirlfriend/Python)
- [JavaScript语言要点](https://cannot.cc/HackGirlfriend/Python)


- [模拟登录抓包](https://cannot.cc/HackGirlfriend/模拟登录抓包)
- [WebSocket入门](https://cannot.cc/HackGirlfriend/WebSocket)
- [SmartQQ协议分析](https://cannot.cc/HackGirlfriend/SmartQQ)
- [uWSGI协议分析](https://cannot.cc/HackGirlfriend/uWSGI)

- [SSH的使用](https://cannot.cc/HackGirlfriend/SSH)
- [Postman的使用](https://cannot.cc/HackGirlfriend/Postman)
- [词库的使用](https://cannot.cc/HackGirlfriend/词库)
- [FunkLoad的试用](https://cannot.cc/HackGirlfriend/FunkLoad)
