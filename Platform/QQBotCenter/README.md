
## 私聊消息数据结构
```json
{
    "result": [
        {
            "poll_type": "group_message", 
            "value": {
                "content": [
                    [
                        "font", 
                        {
                            "color": "000000", 
                            "name": "微软雅黑", 
                            "size": 10, 
                            "style": [
                                0, 
                                0, 
                                0
                            ]
        
}                }
                    ], 
                    "你又在干嘛😂"
                ], 
                "from_uin": 1895510692, 
                "group_code": 1895510692, 
                "msg_id": 27077, 
                "msg_type": 4, 
                "send_uin": 544970383, 
                "time": 1499702517, 
                "to_uin": 491976401
            }
        }
    ], 
    "retcode": 0
```

获取聊天内容：`QMessage.get_msg_content(content)`