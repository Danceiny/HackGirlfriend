# -*- coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import trace
# from PackageNormalData import *
from flask import Blueprint, request, jsonify, redirect, render_template

import pylab
from scipy.io import wavfile

class GirlVoice():
    def __init__(self,raw_voice_robot,params=None):
        #TODO: raw_voice_robot 可以是文件（文件类型），也可以是比特流
        self.raw_voice_robot = raw_voice_robot

    def getBasicPropertyOfVoice(self,voice):
        sampFreq, snd = wavfile.read(voice)
        return snd.dtype, snd.shape

    def getBasicProcessedVoice(self,raw_voice):
        sampFreq, snd = wavfile.read(raw_voice)
        return voice