import time
import json
import requests
import datetime
import traceback
import urllib.request
from . import image_hosting
from flask_cors import cross_origin
from flask import session, redirect, url_for, current_app, flash, Response, request, jsonify
from ..login.login_funtion import User
from ..privilege.privilege_control import permission_required
from ..response import Response
from peewee import DoesNotExist
from ..model.image_hosting_model import image_hosting as image_hosting_table

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


@image_hosting.route('/get', methods=['POST'])
def get():
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