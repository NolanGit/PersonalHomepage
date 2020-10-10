import time
import json
import datetime
import traceback
from . import widget as widget_blue_print
from flask_cors import cross_origin
from flask import session, redirect, url_for, current_app, request, jsonify

from ..login.login_funtion import User
from ..model.widget_model import widget_suite
from ..response import Response as MyResponse
from ..model.widget_model import widget as widget_table
from ..privilege.privilege_control import permission_required
from .widget_fuction import Widget, widget_suite_get, widget_get, widget_all, widget_suite_delete

rsp = MyResponse()
URL_PREFIX = '/widget'


@widget_blue_print.route('/suite/get', methods=['POST'])
#@permission_required(URL_PREFIX + '/suite/get')
def widgetSuite():
    try:
        try:
            user_id = request.get_json()['user_id']
        except:
            user_id = 0
        return rsp.success(widget_suite_get(user_id))
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@widget_blue_print.route('/get', methods=['POST'])
#@permission_required(URL_PREFIX + '/get')
def widget():
    try:
        user_id = request.get_json()['user_id']
        widget_suite_id = request.get_json()['widget_suite_id']
        return rsp.success(widget_get(user_id, widget_suite_id))
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@widget_blue_print.route('/get_all', methods=['POST'])
@permission_required(URL_PREFIX + '/get_all')
def widget_get_all():
    try:
        return rsp.success(widget_all())
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@widget_blue_print.route('/suite/detail', methods=['POST'])
@permission_required(URL_PREFIX + '/suite/detail')
def widgetSuiteDetail():
    try:
        user_id = request.get_json()['user_id']
        _r = widget_suite_get(user_id)
        for x in range(len(_r)):
            _r[x]['widget_detail'] = widget_get(user_id, _r[x]['id'])
        return rsp.success(_r)
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@widget_blue_print.route('/suite/save', methods=['POST'])
@permission_required(URL_PREFIX + '/suite/save')
def widgetSuiteSave():
    try:
        user_id = request.get_json()['user_id']
        suite_data = request.get_json()['suite_data']
        _status, _msg = widget_suite_delete(user_id)
        if not _status:
            raise Exception(_msg)
        data = []
        for s_suite_data in suite_data:
            data.append((s_suite_data['name'], user_id, s_suite_data['order'], 1, s_suite_data['detail'], datetime.datetime.now()))
        field = [widget_suite.name, widget_suite.user_id, widget_suite.order, widget_suite.is_valid, widget_suite.detail, widget_suite.update_time]
        widget_suite.insert_many(data, field).execute()
        return rsp.success()
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500
