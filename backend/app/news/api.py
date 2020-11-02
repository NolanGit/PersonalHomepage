import time
import json
import requests
import datetime
import traceback
from flask_cors import cross_origin
from flask import render_template, session, redirect, url_for, current_app, flash, request, jsonify

from ..common_func import CommonFunc
from ..login.login_funtion import User
from ..response import Response as MyResponse
from ..privilege.privilege_control import privilegeFunction
from ..privilege.privilege_control import permission_required

from . import news

cf = CommonFunc()
rsp = MyResponse()


@news.route('/get', methods=['POST'])
def get():
    try:
        r = json.load('./json/baidu_now.json')
        return rsp.success(r)
    except Exception as e:
        traceback.print_exc()
        return rsp.failed(e), 500
