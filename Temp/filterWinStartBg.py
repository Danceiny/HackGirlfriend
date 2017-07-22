#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
__author__ = 'Danceiny'
__doc__ = """
本模块实现以下功能：
2017-07-15 22:45:27 更新：支持Chrome插件Momentum的背景图。
1. 将Win10开机时的背景图片(DIR)复制到指定目录(PIC_DIR)，并根据文件类型重命名。
2. 删除指定目录下不适合作为桌面背景（不满足DEFAULT_RESOLUTION）的图片。

使用方法：
在以下代码中的【自定义背景】区自定义你的变量，然后直接运行本文件： python filterWinStartBg.py, 再到【Windows设置】-【个性化】-【背景】-【背景】选择【幻灯片放映】，【为幻灯片选择相册】设置为PIC_DIR.

！！！！即可将Win10开机时的好看的背景图设置为桌面幻灯片背景啦！！！！！！
！！！！适用环境！！！！
1. Win10
2. Python2/3
3. pip install pillow

Copyrights @ Danceiny 2017-07-09 Morning
Danceiny@GitHub && danceiny@gmail.com


还可参考：[python 设置windows桌面背景（从网络抓取）](http://www.cnblogs.com/qianlifeng/archive/2012/05/10/2494005.html)
"""
import os
import shutil  # for copy/move file
import imghdr  # determine img type


######################  自定义常量   ####################
USERNAME = 'huangzhen'
MOMENTUM_VER = '0.95.3_0'   # chrome 插件 momontum的版本号,可根据下面代码中的MOMENTUM_DIR进入文件管理器中查找
PIC_DIR = r''
DEFAULT_RESOLUTION = (1920,1080)
######################  自定义常量   ####################

DIR = r'C:/Users/{}/AppData/Local/Packages/Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy/LocalState/Assets'.format(USERNAME)
MOMENTUM_DIR = r'C:/Users\{USER}\AppData\Local\Google\Chrome\User Data\Default\Extensions\laookkfknpbbblfpciffpaejjkokdgca\{VERSION}\backgrounds'.format(USER=USERNAME,VERSION=MOMENTUM_VER)
PIC_DIR = r'C:/Users/{}/Documents/Beautiful/Background'.format(USERNAME) if PIC_DIR == '' else PIC_DIR
DIR = DIR.replace('/','\\')
PIC_DIR = PIC_DIR.replace('/','\\')


def rename(path):
    for filename in os.listdir(path):
        all_filename = os.path.join(path,filename)
        if os.path.isfile(all_filename):
            if filename.find('.') < 0:
                img_type = imghdr.what(all_filename)
                suffix = 'jpg'
                if img_type == 'png':
                    suffix = 'png'
                elif img_type == 'gif':
                    suffix = 'gif'
                elif img_type == None:
                    os.remove(all_filename)
                    continue
                newname = '.'.join((all_filename,suffix))
                os.rename(all_filename,newname)

def copyfiles(oldpath, newpath):
    if not os.path.exists(newpath):
        print('你指定的目录不存在，我要创建它^_^')
        os.makedirs(newpath)
    for filename in os.listdir(oldpath):
        all_old = os.path.join(oldpath, filename)
        if os.path.isfile(all_old):
            is_exist_flag = False
            for newfilename in os.listdir(newpath):
                if newfilename.split('.')[0] == filename:
                    is_exist_flag = True
                    print(' '.join(('目标目录已经存在该文件',filename,'我不会复制它的。')))
                    break
            if is_exist_flag == False:
                shutil.copyfile(all_old, os.path.join(newpath, filename))

from PIL import Image
def get_img_resolution(filename):
    # img = Image.open(filename)
    # imgSize = img.size #图片的长和宽
    # maxSize = max(imgSize) #图片的长边
    # minSize = min(imgSize) #图片的短边
    # return imgSize
    return Image.open(filename).size

def del_unfit_imgs(path,mode='strict'):
    #'strict'模式下删除该路径下所有尺寸不是DEFAULT_RESOLUTION的图片，非stric模式下删除长宽均小于默认尺寸的图片（momentum有很多不满足我原来设想的标准尺寸要求的美图啊~~~）
    for filename in os.listdir(path):
        all_filename = os.path.join(path,filename)
        if os.path.isfile(all_filename):
            if imghdr.what(all_filename) == None:
                os.remove(all_filename)
                continue
            imgSize = get_img_resolution(all_filename)
            if mode == 'strict':
                if max(imgSize) != max(DEFAULT_RESOLUTION) and min(imgSize) != min(DEFAULT_RESOLUTION):
                    os.remove(all_filename)
            else:
                if max(imgSize) < max(DEFAULT_RESOLUTION) and min(imgSize) < min(DEFAULT_RESOLUTION):
                    os.remove(all_filename)

if __name__ == '__main__':
    copyfiles(DIR, PIC_DIR)
    copyfiles(MOMENTUM_DIR,PIC_DIR)
    rename(PIC_DIR)
    del_unfit_imgs(PIC_DIR,mode='non_strict')