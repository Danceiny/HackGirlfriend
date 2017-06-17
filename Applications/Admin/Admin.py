# -*- coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import trace
# from PackageNormalData import *
from flask import Blueprint, request, jsonify, redirect, render_template
import requests
import urllib
from Libraries.Utils import *


# 实例化一个blueprint
Admin = Blueprint("Admin", __name__)

@Admin.route('/')
def hello_world():
    return 'hello_world'