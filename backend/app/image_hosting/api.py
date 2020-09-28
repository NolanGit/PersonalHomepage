import time
import json
import requests
import datetime
import traceback
import configparser
import urllib.request
from peewee import DoesNotExist
from flask_cors import cross_origin
from flask import session, redirect, url_for, current_app, flash, Response, request, jsonify

from . import image_hosting
from ..common_func import CommonFunc
from ..login.login_funtion import User
from ..short_url.function import set_content
from ..response import Response as MyResponse
from ..privilege.privilege_control import permission_required
from ..model.image_hosting_model import image_hosting as image_hosting_table
from ..model.upload_model import upload as upload_table

cf = configparser.ConfigParser()
cf.read('app/homepage.config')
DOMAIN_NAME = cf.get('config', 'DOMAIN_NAME')

cf = CommonFunc()
rsp = MyResponse()

URL_PREFIX = '/imageHosting'


@image_hosting.route('', methods=['GET'])
def fetch():
    t = request.args.get('t')
    try:
        _ = image_hosting_table.get(image_hosting_table.token == t)
        _path = _.file_path
    except DoesNotExist:
        return rsp.failed('找不到文件')
    with open(_path, 'rb') as f:
        image = f.read()
    img = Response(image, mimetype="image/jpeg")
    return img


@image_hosting.route('/get', methods=['POST'])
@permission_required(URL_PREFIX + '/get')
def get():
    try:
        user_id = request.get_json()['user_id']
        _current_page = request.get_json()['current_page']
        _pagination_size = request.get_json()['pagination_size']
        _ = image_hosting_table.select().where((image_hosting_table.user_id == user_id) & (image_hosting_table.is_valid == 1))
        _total = _.count()
        _r = _.order_by(-image_hosting_table.update_time).paginate(_current_page, _pagination_size).dicts()
        _list = [{'id': s_['id'], 'file_name': s_['file_name'], 'shorted_link': s_['shorted_link'], 'update_time': s_['update_time'].strftime("%Y-%m-%d %H:%M:%S")} for s_ in _r]
        return rsp.success({'list': _list, 'total': _total})
    except Exception as e:
        return rsp.failed(e), 500


@image_hosting.route('/save', methods=['POST'])
@permission_required(URL_PREFIX + '/save')
def save():
    try:
        file_id = request.get_json()['file_id']
        _ = upload_table.get(upload_table.id == file_id)
        file_name = _.file_name
        file_path = _.file_path
        user_id = _.user_id
        token = cf.md5_it(file_name.split('.')[0] + str(time.time()).split('.')[0][-6:])
        raw_link = DOMAIN_NAME + URL_PREFIX + '?' + 't=' + str(token)
        shorted_link = set_content(raw_link)  # 存储短链接
        image_hosting_table.create(file_name=file_name, file_path=file_path, token=token, shorted_link=shorted_link, user_id=user_id, is_valid=1, update_time=datetime.datetime.now())
        return rsp.success()
    except Exception as e:
        return rsp.failed(e), 500


@image_hosting.route('/delete', methods=['POST'])
@permission_required(URL_PREFIX + '/delete')
def delete():
    try:
        user_id = request.get_json()['user_id']
        id = request.get_json()['id']
        _ = image_hosting_table.get(image_hosting_table.id == id)
        if int(_.user_id) != int(user_id):
            return rsp.refuse('文件归属错误！'), 403
        else:
            _.token = _.token + '[deleted:' + str(time.time()) + ']'
            _.is_valid = 0
            _.save()
            return rsp.success()
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500


@image_hosting.route('/changeName', methods=['POST'])
@permission_required(URL_PREFIX + '/changeName')
def changeName():
    try:
        user_id = request.get_json()['user_id']
        id = request.get_json()['id']
        file_name = request.get_json()['file_name']
        _ = image_hosting_table.get(image_hosting_table.id == id)
        if int(_.user_id) != int(user_id):
            return rsp.refuse('文件归属错误！'), 403
        else:
            _.file_name = file_name
            _.save()
        return rsp.success()
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500
