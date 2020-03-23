import time
import json
import requests
import datetime
import traceback
import urllib.request
from . import push
from flask_cors import cross_origin
from flask import session, redirect, url_for, current_app, flash, Response, request, jsonify
from ..login.login_funtion import User
from ..privilege.privilege_control import permission_required
from .push_function import PushData, PushList, PushQueueList

URL_PREFIX = '/push'


@push.route('/get', methods=['POST'])
@permission_required(URL_PREFIX + '/get')
@cross_origin()
def get():
    try:
        user_id = request.get_json()['user_id']
        widget_id = request.get_json()['widget_id']
        push_list = PushList(user_id=user_id, widget_id=widget_id).push_list_get().push_list
        if len(push_list) > 1:
            raise Exception('Bad Data Returned, Check The Parameter!')
        response = {'code': 200, 'msg': '成功！', 'data': [] if len(push_list) == 0 else push_list[0].convert_to_dict}
        return jsonify(response)

    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response), 500


@push.route('/add', methods=['POST'])
@permission_required(URL_PREFIX + '/add')
@cross_origin()
def add():
    try:
        PushData(
            user_id=request.get_json()['user_id'],
            widget_id=request.get_json()['widget_id'],
            notify=request.get_json()['notify'],
            notify_method=request.get_json()['notify_method'],
            notify_interval_raw=request.get_json()['notify_interval_raw'],
            notify_interval_unit=request.get_json()['notify_interval_unit'],
            notify_interval=request.get_json()['notify_interval'],
            notify_trigger_time=request.get_json()['notify_trigger_time'],
            update_time=request.get_json()['update_time']).save()
        response = {'code': 200, 'msg': '成功！'}
        return jsonify(response)

    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response), 500


@push.route('/delete', methods=['POST'])
@permission_required(URL_PREFIX + '/delete')
@cross_origin()
def delete():
    try:
        PushData(id=request.get_json()['id']).delete()
        response = {'code': 200, 'msg': '成功！'}
        return jsonify(response)

    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response), 500


@push.route('/edit', methods=['POST'])
@permission_required(URL_PREFIX + '/edit')
@cross_origin()
def edit():
    try:
        PushData(id=request.get_json()['id']).delete()
        PushData(
            user_id=request.get_json()['user_id'],
            widget_id=request.get_json()['widget_id'],
            notify=request.get_json()['notify'],
            notify_method=request.get_json()['notify_method'],
            notify_interval_raw=request.get_json()['notify_interval_raw'],
            notify_interval_unit=request.get_json()['notify_interval_unit'],
            notify_interval=request.get_json()['notify_interval'],
            notify_trigger_time=request.get_json()['notify_trigger_time'],
            update_time=request.get_json()['update_time']).save()
        response = {'code': 200, 'msg': '成功！'}
        return jsonify(response)

    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response), 500