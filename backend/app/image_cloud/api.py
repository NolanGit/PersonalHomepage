import time
import json
import requests
import datetime
import traceback
import urllib.request
from . import image_cloud
from flask_cors import cross_origin
from flask import session, redirect, url_for, current_app, flash, Response, request, jsonify
from ..login.login_funtion import User
from ..privilege.privilege_control import permission_required
from ..response import Response
from peewee import DoesNotExist
from ..model.image_model import image as image_table

rsp = Response()

URL_PREFIX = '/image'


@image_cloud.route('/', methods=['GET'])
def get():
    t = request.args.get('t')
    try:
        _ = image_table.get(image_table.token == t)
        _path = _.file_path
    except DoesNotExist:
        return rsp.failed('找不到文件')
    with open(_path, 'rb') as f:
        image = f.read()
    img = Response(image, mimetype="image/jpeg")
    return img