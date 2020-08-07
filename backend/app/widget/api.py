import time
import json
import datetime
import traceback
from . import widget as widget_blue_print
from flask_cors import cross_origin
from flask import session, redirect, url_for, current_app, request, jsonify

from ..response import Response
from ..login.login_funtion import User
from ..privilege.privilege_control import permission_required
from .widget_fuction import Widget, widget_suite_get, widget_get
from ..model.widget_model import widget as widget_table
from ..model.widget_model import widget_suite

rsp = Response()
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
        return rsp.success(widget_suite_get(user_id))
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e)


@widget_blue_print.route('/suite/detail', methods=['POST'])
@permission_required(URL_PREFIX + '/suite/detail')
@cross_origin()
def widgetSuiteDetail():
    try:
        user_id = request.get_json()['user_id']
        _r = widget_suite_get(user_id)
        for x in range(len(_r)):
            _r[x]['widget_detail'] = widget_get(user_id, _r[x]['id'])
        return rsp.success(_r)
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e)


@widget_blue_print.route('/suite/save', methods=['POST'])
#@permission_required(URL_PREFIX + '/suite/save')
@cross_origin()
def widgetSuiteSave():
    try:
        try:
            user_id = request.get_json()['user_id']
        except:
            user_id = 0
        return rsp.success(widget_suite_get(user_id))
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e)


@widget_blue_print.route('/get', methods=['POST'])
#@permission_required(URL_PREFIX + '/get')
@cross_origin()
def widget():
    try:
        user_id = request.get_json()['user_id']
        widget_suite_id = request.get_json()['widget_suite_id']
        return rsp.success(widget_get(user_id, widget_suite_id))
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e)