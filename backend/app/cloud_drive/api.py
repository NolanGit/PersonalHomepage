import time
import json
import datetime
import traceback
import configparser
from flask_cors import cross_origin
from . import cloud_drive as cloud_drive_blue_print
from flask import session, redirect, current_app, request, jsonify

from ..response import Response
from ..common_func import CommonFunc
from ..model.upload_model import cloud_drive, upload
from ..privilege.privilege_control import privilegeFunction
from ..privilege.privilege_control import permission_required
from ..short_url.function import set_content

cf = configparser.ConfigParser()
cf.read('app/homepage.config')
DOMAIN_NAME = cf.get('config', 'DOMAIN_NAME')

common_func = CommonFunc()
rsp = Response()
URL_PREFIX = '/cloudDrive'


@cloud_drive_blue_print.route('/save', methods=['POST'])
@permission_required(URL_PREFIX + '/save')
def save():
    try:
        user_id = request.get_json()['user_id']
        file_id = request.get_json()['file_id']
        cloud_drive.create(file_id=file_id, user_id=user_id, share_token=None, is_valid=1, update_time=datetime.datetime.now()).save()
        return rsp.success()
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@cloud_drive_blue_print.route('/get', methods=['POST'])
@permission_required(URL_PREFIX + '/get')
def get():
    try:
        user_id = request.get_json()['user_id']
        _current_page = request.get_json()['current_page']
        _pagination_size = request.get_json()['pagination_size']

        user_key = request.cookies.get('user_key')
        redis_conn = privilegeFunction().get_redis_conn0()

        # 判断user_key是否有效
        if user_key == None or redis_conn.exists(user_key) == 0:
            return rsp.failed('错误的用户信息'), 403

        # 判断user_id是否一致
        redis_user_id = redis_conn.get(user_key)
        if int(redis_user_id) != int(user_id):
            return rsp.failed('错误的用户信息'), 403

        _ = cloud_drive.select().where((cloud_drive.user_id == user_id) & (cloud_drive.is_valid == 1))
        _total = _.count()
        _r = _.order_by(-cloud_drive.update_time).paginate(_current_page, _pagination_size).dicts()
        _list = [{
            'id': s_['id'],
            'file_id': s_['file_id'],
            'file_name': upload.get(upload.id == s_['file_id']).file_name,
            'size': upload.get(upload.id == s_['file_id']).size,
            'share': 1 if s_['share_token'] != None and s_['share_token'] != '' else 0,
            'share_link': s_['share_link'],
            'share_expire_time': s_['share_expire_time'].strftime("%Y-%m-%d %H:%M:%S") if s_['share_expire_time'] != None and s_['share_expire_time'] != '' else None,
            'update_time': s_['update_time'].strftime("%Y-%m-%d %H:%M:%S"),
        } for s_ in _r]
        return rsp.success({'list': _list, 'total': _total})
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@cloud_drive_blue_print.route('/delete', methods=['POST'])
@permission_required(URL_PREFIX + '/delete')
def delete():
    try:
        user_id = request.get_json()['user_id']
        id = request.get_json()['id']
        _ = cloud_drive.get(cloud_drive.id == id)
        if int(_.user_id) != int(user_id):
            return rsp.refuse('文件归属错误！'), 403
        else:
            _.is_valid = 0
            _.save()
            return rsp.success()
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@cloud_drive_blue_print.route('/share/set', methods=['POST'])
@permission_required(URL_PREFIX + '/share/set')
def share_set():
    try:
        user_id = request.get_json()['user_id']
        id = request.get_json()['id']

        user_key = request.cookies.get('user_key')
        redis_conn = privilegeFunction().get_redis_conn0()

        # 判断user_key是否有效
        if user_key == None or redis_conn.exists(user_key) == 0:
            return rsp.failed('错误的用户信息'), 403

        # 判断user_id是否一致
        redis_user_id = redis_conn.get(user_key)
        if int(redis_user_id) != int(user_id):
            return rsp.failed('错误的用户信息'), 403

        # 判断文件归属权
        _ = cloud_drive.get(cloud_drive.id == id)
        if int(_.user_id) != int(user_id):
            return rsp.refuse('文件归属错误！'), 403

        salt = common_func.random_str(40)
        token = common_func.md5_it(str(_.id) + str(_.file_id) + salt)
        raw_link = DOMAIN_NAME + '/download?' + 'file_id=' + str(_.file_id) + '&' + 'share_token=' + token
        default_expire_time = datetime.datetime.now() + datetime.timedelta(weeks=100 * 52)  # 有效期覆盖社会主义初级阶段

        _.share_token = token
        _.share_link = set_content(raw_link)  # 存储短链接
        _.share_expire_time = default_expire_time
        _.save()

        return rsp.success()

    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@cloud_drive_blue_print.route('/share/cancel', methods=['POST'])
@permission_required(URL_PREFIX + '/share/cancel')
def cancel():
    try:
        user_id = request.get_json()['user_id']
        id = request.get_json()['id']

        user_key = request.cookies.get('user_key')
        redis_conn = privilegeFunction().get_redis_conn0()

        # 判断user_key是否有效
        if user_key == None or redis_conn.exists(user_key) == 0:
            return rsp.failed('错误的用户信息'), 403

        # 判断user_id是否一致
        redis_user_id = redis_conn.get(user_key)
        if int(redis_user_id) != int(user_id):
            return rsp.failed('错误的用户信息'), 403

        # 判断文件归属权
        _ = cloud_drive.get(cloud_drive.id == id)
        if int(_.user_id) != int(user_id):
            return rsp.refuse('文件归属错误！'), 403

        _.share_token = None
        _.save()

        return rsp.success()
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500

@cloud_drive_blue_print.route('/changeName', methods=['POST'])
@permission_required(URL_PREFIX + '/changeName')
def changeName():
    try:
        user_id = request.get_json()['user_id']
        file_id = request.get_json()['file_id']
        file_name = request.get_json()['file_name']
        _ = upload.get(upload.id == file_id)
        if int(_.user_id) != int(user_id):
            return rsp.refuse('文件归属错误！'), 403
        else:
            _.file_name = file_name
            _.save()
        return rsp.success()
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500