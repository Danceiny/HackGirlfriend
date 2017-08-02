# -*- coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import trace
from flask import Blueprint, request, jsonify, redirect,render_template,url_for


from Libraries.Utils import *
from Libraries.ErrorDefine import *
# 实例化一个blueprint
NBA = Blueprint("NBA", __name__,template_folder='templates',static_folder='static',
                  static_url_path='nba/static')
from Libraries.mythreadpool import *
from Platform.NBACenter.NBACenter import *
nbaCenter = NBACenter.instance()

@NBA.route('nba/huanren',methods=['GET'],endpoint='nba_substitution_patterns')
@check_api_cost_time
@allow_cross_domain
@package_json_request_data
def substitution_patterns():
    data = request.data
    if 'update' in data:
        celery_substitution_patterns.apply_async()

    countryCode = getCountryCode(data['ip'])
    template = 'nba_substitution_crawler.html'
    if countryCode != 'CN' and not data['ip'].startswith('192.168') or data.get('lan','cn') != 'cn':
        template = 'substitution_patterns_en.html'
    return render_template(template)


@NBA.route('longtask', methods=['GET'])
def longtask():
    task = long_task.apply_async()
    return jsonify({}), 202, {'Location': url_for('taskstatus',
                                                  task_id=task.id)}


@NBA.route('status/<task_id>')
def taskstatus(task_id):
    task = long_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        # // job did not start yet
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)