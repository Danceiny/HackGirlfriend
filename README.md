# Hack Girlfriend

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
    - [*] 接入百度语音REST API
    - 接入讯飞API，需要做其他语言到python的桥接，待定
    - fmod api的python接口实现，难度较大，不如直接在其他平台原生实现。
    

# Refs

1. 利用深度学习生成好听的音乐 http://deeplearning.net/tutorial/rnnrbm.html

2. 利用fmod api在Android 实现qq变声效果
http://blog.csdn.net/a847427920/article/details/72831185

3. 从python脚本使用fmod api
http://www.fmod.org/questions/question/how-to-use-fmod-from-a-python-script/

4. MySound: 仿QQ语音变声功能实现(fmod)
- http://codecloud.net/145676.html

- https://github.com/CN-ZPH/MySound.git


5. python音频处理库 http://librosa.github.io


6. Python的C/C 扩展之Python直接调用科大讯飞语音识别动态库 https://zuciwang.com/show/774129.html

必应语音 API

将语音转换为文本，再转回语音，并理解用户的意图

5,000 个事务，每个功能每分钟 20 个。
此 API 密钥当前处于活动状态

剩余 30 天

终结点: https://api.cognitive.microsoft.com/sts/v1.0

密钥 1: 3c46f936d94147e889a8983427de390d

密钥 2: 8cabf4961b264d23b1897a962ebe3abe