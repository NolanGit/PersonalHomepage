import time
import json
import datetime
import traceback
from flask_cors import cross_origin
from . import notes as notes_blue_print
from flask import session, redirect, current_app, request, jsonify

from ..response import Response
from ..login.login_funtion import User
from ..model.push_model import push_queue
from ..model.notes_model import notes as notes_table
from ..privilege.privilege_control import privilegeFunction
from ..privilege.privilege_control import permission_required

rsp = Response()
URL_PREFIX = '/notes'


@notes_blue_print.route('/get', methods=['POST'])
@permission_required(URL_PREFIX + '/get')
def get():
    try:
        user_id = request.get_json()['user_id']
        notes_table_query = notes_table.select().where((notes_table.user_id == user_id) & (notes_table.is_valid == 1)).dicts()
        return rsp.success([{
            'id': _['id'],
            'name': _['name'],
            'token': _['token'],
            'content': _['content'],
            'user_id': _['user_id'],
            'is_valid': _['is_valid'],
            'update_time': _['update_time'],
        } for _ in notes_table_query])
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@notes_blue_print.route('/save', methods=['POST'])
@permission_required(URL_PREFIX + '/save')
def save():
    try:
        user_id = request.get_json()['user_id']
        notes = request.get_json()['notes']
        notes_table.update(is_valid=0).where((notes_table.user_id == user_id) & (notes_table.is_valid == 1)).execute()
        for note in notes:
            if 'id' in note:
                del note['id']
            note['user_id'] = user_id
            note['is_valid'] = 1
            note['update_time'] = datetime.datetime.now()
            notes_table.create(**note)
        return rsp.success()
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@notes_blue_print.route('/notify', methods=['POST'])
@permission_required(URL_PREFIX + '/notify')
def notify():
    try:
        _ = request.get_json()
        notify_trigger_time = datetime.datetime.strptime(_['notify_trigger_time'], "%Y-%m-%d %H:%M") - datetime.timedelta(minutes=1)
        if notify_trigger_time < datetime.datetime.now():
            return rsp.failed('定时运行时间不可以小于当前时间'), 500

        user_id = _['user_id']
        title = _['title']
        content = _['content']
        method = int(_['method'])

        user = User(user_id=user_id)
        if method == 1:
            address = user.wechat_key
        elif method == 2:
            address = user.email
        else:
            return rsp.failed('错误的推送方式'), 500

        push_queue.create(
            user_id=user_id,
            method=method,
            address=address,
            title=title,
            content=content,
            status=0,
            trigger_time=notify_trigger_time,
            log="",
            create_time=datetime.datetime.now(),
            update=datetime.datetime.now())
        return rsp.success()
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@notes_blue_print.route('/revert', methods=['POST'])
@permission_required(URL_PREFIX + '/revert')
def revert():
    try:
        user_id = request.get_json()['user_id']
        user = User(user_id=user_id)
        _ = notes_table.select().where(notes_table.user_id == user_id).group_by(notes_table.update_time).order_by(-notes_table.update_time).limit(6).dicts()
        _r = []
        for s_ in _[1:]:
            _n = notes_table.select().where((notes_table.user_id == user_id) & (notes_table.update_time == s_['update_time'])).dicts()
            _r.append({'update_time': s_['update_time'].strftime("%Y-%m-%d %H:%M:%S"), 'user': user.user_name, 'detail': []})
            for s_n in _n:
                _r[-1]['detail'].append({
                    'id': s_n['id'],
                    'name': s_n['name'],
                    'token': s_n['token'],
                    'content': s_n['content'],
                    'user_id': s_n['user_id'],
                    'is_valid': s_n['is_valid'],
                    'update_time': s_n['update_time']
                })
        return rsp.success(_r)
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500
