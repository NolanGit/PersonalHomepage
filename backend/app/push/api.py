import time
import json
import requests
import datetime
import traceback
import urllib.request
from . import push
from flask_cors import cross_origin
from flask import session, redirect, url_for, current_app, flash, Response, request, jsonify

from ..response import Response
from ..login.login_funtion import User
from ..privilege.privilege_control import permission_required
from .push_function import PushData, PushList, PushQueueList

rsp = Response()

URL_PREFIX = '/push'
CODE_MINUTES = 0  # 库中0代表分钟
CODE_HOUR = 1  # 库中1代表小时
CODE_DAY = 2  # 库中2代表天
HOUR_MINUTES = 60  # 每小时有60分钟
DAY_HOURS = 24  # 每天有24小时


@push.route('/get', methods=['POST'])
@permission_required(URL_PREFIX + '/get')
def get():
    try:
        user_id = request.get_json()['user_id']
        widget_id = request.get_json()['widget_id']
        push_list = PushList(user_id=user_id, widget_id=widget_id).push_list_get().push_list
        if len(push_list) > 1:
            raise Exception('Bad Data Returned, Check The Parameter!')
        return rsp.success([] if len(push_list) == 0 else push_list[0].convert_to_dict())

    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@push.route('/add', methods=['POST'])
@permission_required(URL_PREFIX + '/add')
def add():
    try:
        notify_interval_raw = request.get_json()['notify_interval_raw']
        notify_interval_unit = request.get_json()['notify_interval_unit']
        if notify_interval_unit == CODE_MINUTES:
            if notify_interval_raw < 5:
                return rsp.failed('定时运行间隔最小为五分钟'), 500
            notify_interval = notify_interval_raw
        if notify_interval_unit == CODE_HOUR:
            notify_interval = notify_interval_raw * HOUR_MINUTES
        elif notify_interval_unit == CODE_DAY:
            notify_interval = notify_interval_raw * DAY_HOURS * HOUR_MINUTES

        notify_trigger_time = datetime.datetime.strptime(request.get_json()['notify_trigger_time'], "%Y-%m-%d %H:%M")
        if notify_trigger_time < datetime.datetime.now():
            response = {
                'code': 500,
                'msg': '定时运行时间不可以小于当前时间',
            }
            return jsonify(response), 500

        user_id = request.get_json()['user_id']
        widget_id = request.get_json()['widget_id']
        push_list = PushList(user_id=user_id, widget_id=widget_id).push_list_get().push_list
        for push_data in push_list:
            push_data.delete()
        PushData(
            user_id=user_id,
            widget_id=widget_id,
            notify=request.get_json()['notify'],
            notify_method=request.get_json()['notify_method'],
            notify_interval_raw=notify_interval_raw,
            notify_interval_unit=notify_interval_unit,
            notify_interval=notify_interval,
            notify_trigger_time=notify_trigger_time,
            update_time=datetime.datetime.now()).save()
        return rsp.success()

    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@push.route('/edit', methods=['POST'])
@permission_required(URL_PREFIX + '/edit')
def edit():
    try:
        notify_interval_raw = request.get_json()['notify_interval_raw']
        notify_interval_unit = request.get_json()['notify_interval_unit']
        if notify_interval_unit == CODE_MINUTES:
            if notify_interval_raw < 5:
                return rsp.failed('定时运行间隔最小为五分钟'), 500
            notify_interval = notify_interval_raw
        if notify_interval_unit == CODE_HOUR:
            notify_interval = notify_interval_raw * HOUR_MINUTES
        elif notify_interval_unit == CODE_DAY:
            notify_interval = notify_interval_raw * DAY_HOURS * HOUR_MINUTES

        notify_trigger_time = datetime.datetime.strptime(request.get_json()['notify_trigger_time'], "%Y-%m-%d %H:%M")
        if notify_trigger_time < datetime.datetime.now():
            return rsp.failed('定时运行时间不可以小于当前时间'), 500

        user_id = request.get_json()['user_id']
        widget_id = request.get_json()['widget_id']
        push_list = PushList(user_id=user_id, widget_id=widget_id).push_list_get().push_list
        for push_data in push_list:
            push_data.delete()
        PushData(
            user_id=user_id,
            widget_id=widget_id,
            notify=request.get_json()['notify'],
            notify_method=request.get_json()['notify_method'],
            notify_interval_raw=notify_interval_raw,
            notify_interval_unit=notify_interval_unit,
            notify_interval=notify_interval,
            notify_trigger_time=notify_trigger_time,
            update_time=datetime.datetime.now()).save()
        return rsp.success()

    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500