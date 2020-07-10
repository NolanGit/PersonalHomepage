import time
import json
import datetime
import traceback
from . import widget as widget_blue_print
from flask_cors import cross_origin
from flask import session, redirect, url_for, current_app, request, jsonify
from ..login.login_funtion import User
from ..privilege.privilege_control import permission_required
from .widget_fuction import Widget, widget_suite_get, widget_get
from ..model.widget_model import widget as widget_table
from ..model.widget_model import widget_suite

URL_PREFIX = 'widget'


@widget_blue_print.route('/suite/get', methods=['POST'])
#@permission_required(URL_PREFIX + '/suite/get')
@cross_origin()
def widgetSuite():
    try:
        try:
            user_id = request.get_json()['user_id']
        except:
            user_id = 0
        response = {'code': 200, 'msg': '成功！', 'data': widget_suite_get(user_id)}
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response), 500


@widget_blue_print.route('/get', methods=['POST'])
#@permission_required(URL_PREFIX + '/get')
@cross_origin()
def widget():
    try:
        widget_suite_id = request.get_json()['widget_suite_id']
        response = {'code': 200, 'msg': '成功！', 'data': widget_get(widget_suite_id)}
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response), 500