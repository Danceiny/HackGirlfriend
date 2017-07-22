```json
{u'result': [{u'poll_type': u'group_message', u'value': {u'group_code': 1750998772, u'msg_type': 4, u'send_uin': 2888753848, u'msg_id': 37513, u'content': [[u'font', {u'color': u'000000', u'style': [0, 0, 0], u'name': u'\u5fae\u8f6f\u96c5\u9ed1', u'size': 10}], u'!about'], u'from_uin': 1750998772, u'time': 1500049694, u'to_uin': 491976401}}], u'retcode': 0}

```
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
        
                    }
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


# 群聊消息

```json
{  
   u'result':[  
      {  
         u'poll_type':u'group_message',
         u'value':{  
            u'group_code':1593175490,
            u'msg_type':4,
            u'send_uin':2148960723,
            u'msg_id':17687,
            u'content':[  
               [  
                  u'font',
                  {  
                     u'color':u'000000',
                     u'style':[  
                        0,
                        0,
                        0
                     ],
                     u'name':u'\u5fae\u8f6f\u96c5\u9ed1',
                     u'size':10
                  }
               ],
               u"NameError:name 'one' is not defined"
            ],
            u'from_uin':1593175490,
            u'time':1499846770,
            u'to_uin':491976401
         }
      }
   ],
   u'retcode':0
}
```