import time
import json
import requests
import datetime
import traceback
import subprocess
import collections
from . import console
from flask_cors import cross_origin
from flask import session, redirect, url_for, current_app, flash, Response, request, jsonify
from ..model.console_model import console as console_model
from ..privilege.privilege_control import permission_required

URL_PREFIX = '/console'


@console.route('/get', methods=['GET'])
@permission_required(URL_PREFIX + '/get')
@cross_origin()
def consoleGet():
    result = []
    try:
        console_model_query = console_model.select().where(console_model.is_valid == 1).order_by(console_model.order).dicts()
        for row in console_model_query:
            result.append({'id': row['id'], 'name': row['name'], 'order': row['order'], 'icon': row['icon'], 'component_name': row['component_name'], 'update_time': row['update_time']})
        response = {'code': 200, 'msg': '成功！', 'data': result}
        return jsonify(response)
    except Exception as e:
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response), 500
