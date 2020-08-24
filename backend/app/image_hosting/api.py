import time
import json
import requests
import datetime
import traceback
import urllib.request
from peewee import DoesNotExist
from flask_cors import cross_origin
from flask import session, redirect, url_for, current_app, flash, Response, request, jsonify

from . import image_hosting
from ..response import Response
from ..common_func import CommonFunc
from ..login.login_funtion import User
from ..short_url.function import set_content
from ..privilege.privilege_control import permission_required
from ..model.image_hosting_model import image_hosting as image_hosting_table

cf = CommonFunc()
rsp = Response()

URL_PREFIX = '/image_hosting'


@image_hosting.route('/', methods=['GET'])
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


@image_hosting.route('/set', methods=['POST'])
def set():
    file_name = request.get_json()['file_name']
    file_path = request.get_json()['file_path']
    token = cf.md5_it(file_name.split('.')[0] + str(time.time()).split('.')[0][-6:])
    raw_link = ''
    share_link = set_content(raw_link)  # 存储短链接
    try:
        pass
    except DoesNotExist:
        return rsp.failed('找不到文件')
