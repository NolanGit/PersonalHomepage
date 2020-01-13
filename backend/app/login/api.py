import time
import json
import redis
import requests
import datetime
import traceback
import subprocess
import urllib.request
from . import login
from .func import CommonFunc
from flask_cors import cross_origin
from flask import render_template, session, redirect, url_for, current_app, flash, Response, request, jsonify
from .model import user
from ..privilege.model import privilege, privilege_role


def get_redis_conn():
    return redis.Redis(connection_pool=redis.ConnectionPool(host='localhost', port=6379, db=1))


def set_user_privilege_to_redis(redis_conn, user_role_id, privilege_key):
    privilege_role_query = privilege_role.select().where(privilege_role.role_id == user_role_id).dicts()
    for single_privilege_role_query in privilege_role_query:
        redis_conn.rpush(privilege_key, privilege.get(privilege.id == single_privilege_role_query['privilege_id']))


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
                    response = {'code': 200, 'msg': '登录成功！', 'user': row['name']}
                    user_key = CommonFunc().random_str(40)
                    privilege_key = CommonFunc().random_str(40)
                    user_dict = {'user_id': row['id'], 'privilege_key': privilege_key}
                    redis_conn = get_redis_conn()
                    redis_conn.hmset(user_key, user_dict)
                    set_user_privilege_to_redis(redis_conn,row['role_id'],privilege_key)
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
