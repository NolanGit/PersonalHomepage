import time
import json
import datetime
import traceback
from flask_cors import cross_origin
from . import cloud_drive as cloud_drive_blue_print
from flask import session, redirect, current_app, request, jsonify

from ..model.upload_model import cloud_drive, upload
from ..privilege.privilege_control import permission_required

URL_PREFIX = '/cloudDrive'


@cloud_drive_blue_print.route('/save', methods=['POST'])
@permission_required(URL_PREFIX + '/save')
@cross_origin()
def save():
    try:
        user_id = request.get_json()['user_id']
        file_id = request.get_json()['file_id']
        cloud_drive.create(file_id=file_id, user_id=user_id, is_valid=1, update_time=datetime.datetime.now()).save()
        response = {'code': 200, 'msg': '成功！', 'data': []}
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response), 500


@cloud_drive_blue_print.route('/get', methods=['POST'])
@permission_required(URL_PREFIX + '/get')
@cross_origin()
def get():
    try:
        user_id = request.get_json()['user_id']
        _ = cloud_drive.select().where(cloud_drive.user_id == user_id & cloud_drive.is_valid == 1).order_by(-cloud_drive.update_time).dicts()
        response = {
            'code': 200,
            'msg': '成功！',
            'data': [{
                'id': s_['id'],
                'file_id': s_['file_id'],
                'file_name': upload.get(upload.id == s_['file_id']).file_name,
                'update_time': s_['update_time'].strftime("%Y-%m-%d %H:%M:%S"),
            } for s_ in _]
        }
        return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response), 500


@cloud_drive_blue_print.route('/delete', methods=['POST'])
@permission_required(URL_PREFIX + '/delete')
@cross_origin()
def delete():
    try:
        user_id = request.get_json()['user_id']
        id = request.get_json()['id']
        _ = cloud_drive.get(cloud_drive.id == id)
        if int(_.user_id) != int(user_id):
            response = {'code': 403, 'msg': '文件归属错误！'}
            return jsonify(response), 403
        else:
            _.is_valid = 0
            _.save()
            response = {'code': 200, 'msg': '成功！'}
            return jsonify(response)
    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response), 500