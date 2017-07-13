# 你好，这里是HackGirlfriend！ 
If [English Prefered](http://cannot.cc/README_EN.md) :shipit::sunglasses:。

HackGirlfriend是我真正意义上的第一个GitHub开源项目，也是一个“系统”的Web服务器后台项目。

我计划将它打造为一个高可扩展性的后台，引入诸如QQ聊天机器人、NBA数据分析、学生组织后台管理等有趣或有着高频次需求的完全独立的、模块化的应用。性能也是追求之一。

由于我基本处于学习中的Web菜鸟阶段以及作为高年级的本科生，也身处技术学校的技术团队，HackGirlfriend将主要用于向高手学习、与网络探究、与同辈交流、指导学弟学妹。

起名是一件有学问的事情。不要把HackGirlfriend打错成 'HackGrilfriend' 或者 'HackGirlfirend'喔^_^（这是我经常干的事情，如果没有Tab自动完成的话）。

## HackGirlfriend是什么？
前文已提到作为“父母”的我所希望的HackGirlfriend是什么。由于项目仍在比较初级的v0.0.1阶段（已上线公网服务器以及较少的功能，但仍长期处于Debug状态），因此这个问题还是等它长大一点再回答吧。

>Google一下HackGirlfriend，这张图令我印象深刻！https://img.wonderhowto.com/img/87/03/63528600955598/0/hack-like-pro-hack-windows-7-see-whether-your-girlfriend-is-cheating-not.1280x600.jpg

## HackGirlfriend能做什么？

由于这是一项进展中的项目，而且要满足“高可扩展性”的验证，以及“有趣的”、“高频次需求的”这些指标，这个列表将会持续更新(按照各项的开始时间排序)。

* [*] 文字转语音，基于百度语音的RESTful API，将文字转为声音文件。目前只完成api的简单转发。（一开始是想拿到百度的声音来做音频处理的，发现难度略大）

* [x] QQ聊天记录分析, 导出QQ聊天记录的txt文件，可得到聊天记录的时间、频次、内容、情感等自然语言处理分析记录。目前是本地运行的应用（暂不支持web端）。

* [x] QQ聊天机器人，支持Web端扫描二维码登录开启基于图灵API的聊天机器人，支持群聊以及私聊，并支持部分参数设置。

* [x] 醉晚亭工作室部门管理后台，会议记录+请假系统+投票系统+成员管理。 

* [ ] Secret App 服务端。[Secret](https://github.com/Danceiny/Secret)是我的一个类似带朋友圈的私密聊天Android项目。
* [ ] NBA数据分析, 基于某项NBA+Programming主题的比赛获奖项目。

与HackGirlfriend强相关的还有本人的姊妹项目[HG-admin](https://github.com/Danceiny/HG-admin)，HackGirlfriend的后台管理系统前端。

# 如何部署HackGirlfriend到你的主机上？

有关部署平台的选择，我在开发中力求兼顾平台兼容性，基本功能在Linux/OS X/Windows上均能正常工作，当然也有平台相关的无能为力。详见[HackGirlfriend的平台兼容性](https://cannot.cc/HackGirlfriend/Platform)

**First, you need know the dependencies of HackGirlfriend.**
See [Dependencies](https://cannot.cc/HackGirlfriend/Dependencies).

**Then, follow the details on how to deploy this project on Ubuntu Server.**
See [DeployWebServer](https://github.com/Danceiny/HackGirlfriend/DeployWebServer).
 
 or See [Docker Deploy](http://cannot.cc/HackGirlfriend/Docker).

# 相关原创文档列表

- [Flask初探以及在HackGirlfriend中的实战应用](http://cannot.cc/HackGirlfriend/Flask)
- [Flask + uWSGI + supervisor在Linux服务器上的部署](http://cannot.cc/HackGirlfriend/DeployWebServer)

- [Docker快速部署](http://cannot.cc/HackGirlfriend/Docker)
- [ThreadPool](http://cannot.cc/HackGirlfriend/ThreadPool)
- [Celery](http://cannot.cc/HackGirlfriend/Celery)

- [Python语言要点](http://cannot.cc/HackGirlfriend/Python)
- [JavaScript语言要点](http://cannot.cc/HackGirlfriend/Python)


- [模拟登录抓包](http://cannot.cc/HackGirlfriend/模拟登录抓包)
- [WebSocket入门](http://cannot.cc/HackGirlfriend/WebSocket)
- [SmartQQ协议分析](http://cannot.cc/HackGirlfriend/SmartQQ)
- [uWSGI协议分析](http://cannot.cc/HackGirlfriend/uWSGI)

- [SSH的使用](http://cannot.cc/HackGirlfriend/SSH)
- [Postman的使用](http://cannot.cc/HackGirlfriend/Postman)
- [词库的使用](http://cannot.cc/HackGirlfriend/词库)
- [FunkLoad的试用](http://cannot.cc/HackGirlfriend/FunkLoad)
