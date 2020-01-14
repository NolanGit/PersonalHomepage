import time
import json
import redis
import requests
import datetime
import traceback
import subprocess
import urllib.request
from . import login
from ..common_func import CommonFunc
from flask_cors import cross_origin
from flask import render_template, session, redirect, url_for, current_app, flash, Response, request, jsonify
from .model import user
from ..privilege.model import privilege, privilege_role
from ..privilege.api import privilegeFunction


class User(object):

    user_name = ''
    user_id = 0

    def __init__(self, user_name):
        self.user_name = user_name
        user_query = user.select().where(user.name == self.user_name).limit(1).dicts()
        for row in user_query:
            self.user_id = row['id']
            self.role = row['role']
            self.create_time = row['create_time']
            self.update_time = row['update_time']


@login.route('/userLogin', methods=['POST'])
@cross_origin()
def userLogin():
    login_name = request.get_json()['login_name']
    password = request.get_json()['password']
    timestamp = request.get_json()['timestamp']
    ip = request.remote_addr
    print('Login name:' + login_name + ' IP:' + str(ip))
    user_query = user.select().where(user.login_name == login_name).dicts()
    if len(user_query) == 0:
        response = {
            'code': 403,
            'msg': '用户名或密码错误！',
        }
        return jsonify(response)
    else:
        for row in user_query:
            password_without_salt = row['password']
            salt_expire_time = row['salt_expire_time']
            salt = row['salt']
            if timestamp < salt_expire_time:
                password2compare = CommonFunc().md5_it(password_without_salt + salt)
                if password == password2compare:
                    user_key = privilegeFunction().init_user_and_privilege(row['id'], row['role_id'])
                    response = {'code': 200, 'msg': '登录成功！', 'user': row['name'], 'user_key': user_key}
                    return jsonify(response)
                else:
                    response = {
                        'code': 403,
                        'msg': '用户名或密码错误！',
                    }
                    return jsonify(response)
            else:
                response = {
                    'code': 403,
                    'msg': '时间戳已过期，请刷新页面！',
                }
                return jsonify(response)


@login.route('/userLoginGetSalt', methods=['POST'])
@cross_origin()
def userLoginGetSalt():
    try:
        login_name = request.get_json()['login_name']
        salt = CommonFunc().random_str(40)
        user_query = user.select().where(user.login_name == login_name).dicts()
        for row in user_query:
            stable_salt = row['stable_salt']
        user.update(salt=salt, salt_expire_time=(int(time.mktime((datetime.datetime.now() + datetime.timedelta(minutes=1)).timetuple())))).where(user.login_name == login_name).execute()
        response = {'code': 200, 'msg': '成功！', 'data': {'salt': salt, 'stable_salt': stable_salt}}
        return jsonify(response)
    except Exception as e:
        response = {'code': 500, 'msg': e, 'data': {}}
        return jsonify(response)
