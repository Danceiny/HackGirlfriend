# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import re
import random
import json
import os

import datetime
import time
import threading
import urllib
from HttpClient import HttpClient
import Utils as util

from CONFIGS import *





class PmchatThread(threading.Thread):

    # con = threading.Condition()
    # newIp = ''

    def __init__(self, tuin, isSess, group_sig, service_type,QMsg_Ist):
        threading.Thread.__init__(self)
        self.tuin = tuin
        self.isSess = isSess
        self.group_sig=group_sig
        self.service_type=service_type
        self.lastcheck = time.time()
        self.lastseq=0
        self.replystreak = 0
        self.QMsg_Ist = QMsg_Ist
        self.HttpClient_Ist = QMsg_Ist.HttpClient_Ist

        logger.info("私聊线程生成，私聊对象UIN："+str(self.tuin))

    def check(self):
        self.lastcheck = time.time()

    def run(self):
        while 1:
            time.sleep(199)
            if time.time() - self.lastcheck > 300:
                break

    def reply(self, content):
        self.QMsg_Ist.send_msg(self.tuin, str(content), self.isSess, self.group_sig, self.service_type)
        logger.info("Reply to " + str(self.tuin) + ":" + str(content))

    def push(self, ipContent, seq):
        if seq == self.lastseq:
            return True
        else:
            self.lastseq=seq
        #防止机器人对聊
        if self.replystreak>30:
            self.replystreak = 0
            return True
        try:
            self.replystreak = self.replystreak + 1
            logger.info("PM get info from AI: "+ipContent)
            if(u"机器人" in ipContent):
                self.open_bot = True
            if(u"关掉吧" in ipContent):
                self.open_bot = False
            if self.open_bot:
                paraf={ 'userid' : str(self.tuin), 'key' : TULING_KEY, 'info' : ipContent}

                info = self.HttpClient_Ist.Get('http://www.tuling123.com/openapi/api?'+urllib.urlencode(paraf))
                logger.info("AI REPLY:"+str(info))
                info = json.loads(info)
                if info["code"] in [40001, 40003, 40004]:
                    self.reply("我今天累了，不聊了")
                    logger.warning("Reach max AI call")
                elif info["code"] in [40002, 40005, 40006, 40007]:
                    self.reply("我遇到了一点问题，请稍后@我")
                    logger.warning("PM AI return error, code:"+str(info["code"]))
                else:
                    rpy = str(info["text"]).replace('<主人>','你').replace('<br>',"\n")
                    self.reply(rpy)
                return True
        except Exception, e:
            logger.error("ERROR:"+str(e))
        return False



class GroupThread(threading.Thread):
    last1 = ''
    lastseq = 0
    replyList = {}
    followList = []
    NickList = {}

    # 属性
    repeatPicture = True

    def __init__(self, guin, gcode,QMsg_Ist):
        threading.Thread.__init__(self)
        self.QMsg_Ist = QMsg_Ist
        self.HttpClient_Ist = QMsg_Ist.HttpClient_Ist
        self.guin = guin
        self.gid = gcode
        self.load()
        self.lastreplytime=0
        ret = self.HttpClient_Ist.Get((GET_GROUP_INFO_URL).format(gcode, self.QMsg_Ist.VFWebQQ, util.get_ts()), REFERER_URL)
        ret = json.loads(ret)
        for t in ret['result']['minfo']:
            self.NickList[str(t["nick"])]=int(t["uin"])

    def learn(self, key, value, needreply=True):
        if key in self.replyList:
            self.replyList[key].append(value)
        else:
            self.replyList[key] = [value]

        if needreply:
            self.reply("我记住" + str(key) + "的回复了")
            self.save()

    def delete(self, key, value, needreply=True):
        if key in self.replyList and self.replyList[key].count(value):
            self.replyList[key].remove(value)
            if needreply:
                self.reply("我已经不会说" + str(value) + "了")
                self.save()

        else:
            if needreply:
                self.reply("没找到你说的那句话哦")

    def reply(self, content):
        if time.time() - self.lastreplytime < 3.0:
            logger.info("REPLY TOO FAST, ABANDON："+content)
            return False
        self.lastreplytime = time.time()
        reqURL = QQ_GROUP_REPLY_URL
        data = (
            ('r', '{{"group_uin":{0}, "face":564,"content":"[\\"{4}\\",[\\"font\\",{{\\"name\\":\\"Arial\\",\\"size\\":\\"10\\",\\"style\\":[0,0,0],\\"color\\":\\"000000\\"}}]]","clientid":{1},"msg_id":{2},"psessionid":"{3}"}}'.format(self.guin, CLIENT_ID, self.QMsg_Ist.msgId, self.QMsg_Ist.PSessionID, util.CProcess(content))),
            ('clientid', CLIENT_ID),
            ('psessionid', self.QMsg_Ist.PSessionID)
        )
        logger.info("Reply package: " + str(data))
        rsp = self.HttpClient_Ist.Post(reqURL, data, HTTPS_REFERER_URL)
        try:
            rspp = json.loads(rsp)
            if rspp['errCode'] == 0:
                logger.info("[Reply to group " + str(self.gid) + "]:" + str(content))
                return True
        except:
            pass
        logger.error("[Fail to reply group " + str(self.gid)+ "]:" + str(rsp))
        return rsp

    def handle(self, send_uin, content, seq):
        # 避免重复处理相同信息
        if seq != self.lastseq:
            pattern = re.compile(r'^(?:!|！)(learn|delete) {(.+)}{(.+)}')
            match = pattern.match(content)
            if match:
                if match.group(1) == 'learn':
                    self.learn(str(match.group(2)).decode('UTF-8'), str(match.group(3)).decode('UTF-8'))
                    logger.debug(self.replyList)
                if match.group(1) == 'delete':
                    self.delete(str(match.group(2)).decode('UTF-8'), str(match.group(3)).decode('UTF-8'))
                    logger.debug(self.replyList)

            else:
                # if not self.follow(send_uin, content):
                #     if not self.tucao(content):
                #         if not self.repeat(content):
                #             if not self.callout(content):
                #                 pass
                if self.aboutme(content):
                    return
                if self.deleteall(content):
                    return
                if self.callout(send_uin, content):
                    return
                if self.follow(send_uin, content):
                    return
                if self.tucao(content):
                    return
                if self.repeat(content):
                    return

        else:
            logger.warning("message seq repeat detected.")
        self.lastseq = seq

    def tucao(self, content):
        for key in self.replyList:
            if str(key) in content and self.replyList[key]:
                rd = random.randint(0, len(self.replyList[key]) - 1)
                self.reply(self.replyList[key][rd])
                logger.info('Group Reply'+str(self.replyList[key][rd]))
                return True
        return False

    def repeat(self, content):
        if self.last1 == str(content) and content != '' and content != ' ':
            if self.repeatPicture or "[图片]" not in content:
                self.reply(content)
                logger.info("已复读：{" + str(content) + "}")
                return True
        self.last1 = content

        return False

    def follow(self, send_uin, content):
        pattern = re.compile(r'^(?:!|！)(follow|unfollow) (.*)!')
        match = pattern.match(content)

        if match:
            target1 = str(match.group(2))
            if target1 == 'me':
                target = send_uin
                target1 = '你'
            else:
                if target1 in self.NickList:
                    target = self.NickList[target1]
                else:
                    self.reply("找不到成员："+target1)
                    return True

            if match.group(1) == 'follow' and target not in self.followList:
                self.followList.append(target)
                self.reply("正在关注" + target1)
                return True
            if match.group(1) == 'unfollow' and target in self.followList:
                self.followList.remove(target)
                self.reply("我不关注" + target1 + "了！")
                return True
        else:
            if send_uin in self.followList:
                self.reply(content)
                return True
        return False

    def save(self):
        try:
            with open("database."+str(self.gid)+".save", "w+") as savefile:
                savefile.write(json.dumps(self.replyList))
                savefile.close()
        except Exception, e:
            logger.error("写存档出错："+str(e))
    def load(self):
        try:
            with open("database."+str(self.gid)+".save", "r") as savefile:
                saves = savefile.read()
                if saves:
                    self.replyList = json.loads(saves)
                savefile.close()
        except Exception, e:
            logger.info("读取存档出错:"+str(e))

    def callout(self, send_uin, content):
        pattern = re.compile(r'^(?:!|！)(ai) (.+)')
        match = pattern.match(content)
        try:
            if match:
                logger.info("get info from AI: "+str(match.group(2)).decode('UTF-8'))
                usr = str(send_uin)
                paraf={ 'userid' : usr+'g', 'key' : TULING_KEY, 'info' : str(match.group(2)).decode('UTF-8')}

                info = self.HttpClient_Ist.Get(TULING_API_URL+urllib.urlencode(paraf))
                logger.info("AI REPLY:"+str(info))
                info = json.loads(info)
                if info["code"] in [40001, 40003, 40004]:
                    self.reply("我今天累了，不聊了")
                    logger.warning("Reach max AI call")
                elif info["code"] in [40002, 40005, 40006, 40007]:
                    self.reply("我遇到了一点问题，请稍后@我")
                    logger.warning("AI return error, code:"+str(info["code"]))
                else:
                    self.reply(str(info["text"]).replace('<主人>','你').replace('<br>',"\n"))
                return True
        except Exception, e:
            logger.error("ERROR"+str(e))
        return False

    def aboutme(self, content):
        pattern = re.compile(r'^(?:!|！)(about)')
        match = pattern.match(content)
        try:
            if match:
                logger.info("output about info")
                info="小黄鸡 v3.9 Modified by Danceiny. See: http://blog.cannot.cc/"
                self.reply(info)
                return True
        except Exception, e:
            logger.error("ERROR"+str(e))
        return False

    def deleteall(self, content):
        pattern = re.compile(r'^(?:!|！)(deleteall)')
        match = pattern.match(content)
        try:
            if match:
                logger.info("Delete all learned data for group:"+str(self.gid))
                info="已删除所有学习内容"
                self.replyList.clear()
                self.save()
                self.reply(info)
                return True
        except Exception, e:
            logger.error("ERROR:"+str(e))
        return False