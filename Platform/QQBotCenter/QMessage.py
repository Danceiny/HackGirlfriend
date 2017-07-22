# -*- coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from QThread import *
from QQBotDBManager import QQBotDBManager
from CONFIGS import *




class QMessage(threading.Thread):
    # try:
    #   pass
    # except KeybordInterrupt:
    #   try:
    #     user_input = (raw_input("回复系统：（输入格式:{群聊2or私聊1}, {群号or账号}, {内容}）\n")).split(",")
    #     if (user_input[0] == 1):

    #       for kv in self.FriendList :
    #         if str(kv[1]) == str(user_input[1]):
    #           tuin == kv[0]

    #       self.send_msg(tuin, user_input[2])

    #   except KeybordInterrupt:
    #     exit(0)
    #   except Exception, e:
    #     print Exception, e

    def __init__(self,HttpClient_Ist,LoginDelegate,params=None):
        threading.Thread.__init__(self)
        self.qqBotDBManager = QQBotDBManager.instance()
        self.PSessionID = LoginDelegate.PSessionID
        self.PTWebQQ = LoginDelegate.PTWebQQ
        self.VFWebQQ = LoginDelegate.VFWebQQ
        self.HttpClient_Ist = HttpClient_Ist
        self.MyUIN = LoginDelegate.MyUIN

        self.ThreadList = []
        self.GroupThreadList = []
        self.GroupWatchList = []    #str(guin)

        # for t in ret['result']['gnamelist']:
        #     self.GroupNameList[str(t["name"])] = int(t["gid"])
        #     self.GroupCodeList[int(t["gid"])] = int(t["code"])

        self.GroupCodeList = {}
        self.GroupNameList = {}
    def run(self):
        E = 0
        # 心跳包轮询
        while 1:
            if E > 5:
                break
            try:
                ret = self.check_msg()
            except:
                E += 1
                continue
            logger.info(ret)

            # 返回数据有误
            if ret == "":
                E += 1
                continue

            # POST数据有误
            if ret['retcode'] == 100006:
                break

            # 无消息
            if ret['retcode'] == 102:
                E = 0
                continue

            # 更新PTWebQQ值
            if ret['retcode'] == 116:
                self.PTWebQQ = ret['p']
                E = 0
                continue

            if ret['retcode'] == 0:
                # 信息分发
                logger.debug('ZuiwanCenter.QMessage check_msg.retcode: %s' % str(ret['retcode']))
                if 'result' in ret:
                    logger.info(ret)
                    self.msg_handler(ret['result'])
                E = 0
                continue
            if ret['retcode'] == 103:
                logger.error('请登录w.q.com，并退出！')
            # Other retcode e.g.: 103
            E += 1
            self.HttpClient_Ist.Get(BUDDY_URL.format(self.VFWebQQ,CLIENT_ID,self.PSessionID,util.get_ts()), REFERER_URL)

        logger.error("轮询错误超过五次")

    # 向服务器查询新消息
    def check_msg(self):

        html = self.HttpClient_Ist.Post(CHECK_MSG_URL, {
            'r': '{{"ptwebqq":"{1}","clientid":{2},"psessionid":"{0}","key":""}}'.format(self.PSessionID, self.PTWebQQ, CLIENT_ID)
        }, HTTPS_REFERER_URL)
        logger.info("Check html: " + str(html))
        try:
            ret = json.loads(html)
        except Exception as e:
            logger.error(str(e))
            logger.error("Check error occured, retrying.")
            return self.check_msg()
        return ret

    def send_msg(self,tuin, content, isSess, group_sig, service_type):
        if isSess == 0:
            reqURL = SEND_BUDDY_MSG_URL
            data = (
                ('r',
                 '{{"to":{0}, "face":594, "content":"[\\"{4}\\", [\\"font\\", {{\\"name\\":\\"Arial\\", \\"size\\":\\"10\\", \\"style\\":[0, 0, 0], \\"color\\":\\"000000\\"}}]]", "clientid":{1}, "msg_id":{2}, "psessionid":"{3}"}}'.format(
                     tuin, CLIENT_ID, self.msgId, self.PSessionID, util.CProcess(content))),
                ('clientid', CLIENT_ID),
                ('psessionid', self.PSessionID)
            )
            rsp = self.HttpClient_Ist.Post(reqURL, data, HTTPS_REFERER_URL)
            rspp = json.loads(rsp)
            if rspp['errCode'] != 0:
                logger.error("reply pmchat error" + str(rspp['errCode']))
        else:
            reqURL = SEND_SESS_MSG_URL
            data = (
                ('r',
                 '{{"to":{0}, "face":594, "content":"[\\"{4}\\", [\\"font\\", {{\\"name\\":\\"Arial\\", \\"size\\":\\"10\\", \\"style\\":[0, 0, 0], \\"color\\":\\"000000\\"}}]]", "clientid":{1}, "msg_id":{2}, "psessionid":"{3}", "group_sig":"{5}", "service_type":{6}}}'.format(
                     tuin, CLIENT_ID, self.msgId, self.PSessionID, util.CProcess(content), group_sig, service_type)),
                ('clientid', CLIENT_ID),
                ('psessionid', self.PSessionID),
                ('group_sig', group_sig),
                ('service_type', service_type)
            )
            rsp = self.HttpClient_Ist.Post(reqURL, data, HTTPS_REFERER_URL)
            rspp = json.loads(rsp)
            if rspp['errCode'] != 0:
                logger.error("reply temp pmchat error" + str(rspp['errCode']))

        return rsp

    def msg_handler(self,msgObj):
        for msg in msgObj:

            data = {}
            data['timestamp'] = msg['value']['time']
            data['pollType'] = msg['poll_type']
            data['content'] = self.get_msg_content(msg['value']['content'])
            data['to_qqNumber'] = msg['value']['to_uin']
            data['msgId'] = '_'.join((str(data['timestamp']),str(msg['value']['msg_id'])))
            # 持久化收到的消息 TODO:如果收到的这条消息是一段对话的开始，将msgId传给子线程
            ret = self.qqBotDBManager.add_records(data)

            msgType = msg['poll_type']
            # QQ私聊消息
            if msgType == 'message' or msgType == 'sess_message':  # 私聊 or 临时对话
                tuin = msg['value']['from_uin']
                msg_id = data['msgId']

                targetThread = util.thread_exist(tuin,self.ThreadList)
                if targetThread:
                    targetThread.push(data['content'], msg_id)
                else:

                    try:
                        service_type = 0
                        isSess = 0
                        group_sig = ''
                        if msgType == 'sess_message':
                            isSess = 1
                            service_type = msg['value']['service_type']
                            myid = msg['value']['id']
                            info = json.loads(self.HttpClient_Ist.Get(
                                MSG_HANDLER_URL.format(myid, tuin, CLIENT_ID, self.PSessionID, service_type, util.get_ts()), REFERER_URL))
                            logger.info("Get group sig:" + str(info))
                            if info['retcode'] != 0:
                                raise ValueError, info
                            info = info['result']
                            group_sig = info['value']

                        tmpThread = PmchatThread(tuin, isSess, group_sig, service_type, self)
                        tmpThread.start()
                        self.ThreadList.append(tmpThread)
                        tmpThread.push(data['content'],msg_id,ret)
                    except Exception, e:
                        logger.info("error"+str(e))

                # print "{0}:{1}".format(self.FriendList.get(tuin, 0), txt)

                # if FriendList.get(tuin, 0) == AdminQQ:#如果消息的发送者与AdminQQ不相同, 则忽略本条消息不往下继续执行
                #     if txt[0] == '#':
                #         thread.start_new_thread(self.runCommand, (tuin, txt[1:].strip(), msgId))
                #         msgId += 1

                # if txt[0:4] == 'exit':
                #     logger.info(self.Get('http://d1.web2.qq.com/channel/logout2?ids=&clientid={0}&psessionid={1}'.format(self.CLIENT_ID, self.PSessionID), REFERER_URL))
                #     exit(0)

            # 群消息
            # {"result": [{"poll_type": "group_message", "value": {
            #     "content": [["font", {"color": "000000", "name": "微软雅黑", "size": 10, "style": [0, 0, 0]}], " 这里修改了还不行"],
            #     "from_uin": 2188322869, "group_code": 2188322869, "msg_id": 32905, "msg_type": 4,
            #     "send_uin": 4171258001, "time": 1499835891, "to_uin": 491976401}}], "retcode": 0}
            if msgType == 'group_message':
                guin = msg['value']['from_uin'] #u'from_uin': 2188322869L
                gid = self.GroupCodeList.get(int(guin)) #u'gid': 3253257675L
                tuin = msg['value']['send_uin']#u'to_uin': 491976401
                seq = msg['value']['msg_id']
                if str(guin) in self.GroupWatchList:
                    g_exist = util.group_thread_exist(gid,self.GroupThreadList)
                    if g_exist:
                        g_exist.handle(tuin, data['content'], seq)
                    else:
                        tmpThread = GroupThread(guin, gid, self)
                        tmpThread.start()
                        self.GroupThreadList.append(tmpThread)
                        tmpThread.handle(tuin, data['content'], seq)
                        logger.info("群线程已生成")
                else:
                    logger.info(str(gid) + "群有动态，但是没有被监控")

            # QQ号在另一个地方登陆, 被挤下线
            if msgType == 'kick_message':
                logger.error(msg['value']['reason'])
                raise Exception, msg['value']['reason']  # 抛出异常, 重新启动WebQQ, 需重新扫描QRCode来完成登陆


    def get_msg_content(self, content):
        msgTXT = ""
        for part in content:
            # print type(part)
            if type(part) == type(u'\u0000'):
                msgTXT += part
            elif len(part) > 1:
                # 如果是图片
                if str(part[0]) == "offpic" or str(part[0]) == "cface":
                    msgTXT += "[图片]"

        return msgTXT

    def watch_group(self):
        self.msgId = int(random.uniform(20000, 50000))
        login_html = self.HttpClient_Ist.Post(QQ_GROUP_API_URL, {
            'r': '{{"vfwebqq":"{0}","hash":"{1}"}}'.format(str(self.VFWebQQ), util.gethash(str(self.MyUIN), str(self.PTWebQQ)))
        }, REFERER_URL)
        ret = json.loads(login_html)

        if ret['retcode'] != 0:
            raise ValueError, "retcode error when getting group list: retcode=" + str(ret['retcode'])
        logger.info('Get Group Name List: ')
        logger.info(ret['result']['gnamelist'])

        for t in ret['result']['gnamelist']:
            self.GroupNameList[str(t["name"])] = int(t["gid"])
            self.GroupCodeList[int(t["gid"])] = int(t["code"])  #gid = self.GroupCodeList[int(guin)]
        self.HttpClient_Ist.Get((BUDDY_URL).format(self.VFWebQQ, CLIENT_ID, self.PSessionID, util.get_ts()), REFERER_URL)
