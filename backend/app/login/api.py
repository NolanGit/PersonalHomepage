import time
import json
import redis
import requests
import datetime
import traceback
import subprocess
import urllib.request
from flask_cors import cross_origin
from flask import session, redirect, url_for, current_app, flash, request, jsonify

from . import login
from ..common_func import CommonFunc
from ..model.login_model import user
from ..privilege.api import privilegeFunction
from ..response import Response as MyResponse

cf = CommonFunc()
rsp = MyResponse()
pf = privilegeFunction()
ALLOWED_TIME_SPAN = 100  # 盐过期X秒内允许修改密码，否则需要重新登录


def check_pass(login_name, password):
    user_query = user.select().where(user.login_name == login_name).dicts()
    if len(user_query) == 0:
        response = {
            'code': 403,
            'msg': '用户名或密码错误！',
        }
        return (False, response)
    else:
        for row in user_query:
            password_without_salt = row['password']
            salt_expire_time = row['salt_expire_time']
            is_valid = row['is_valid']
            salt = row['salt']
            server_timestamp = datetime.datetime.now()
            if is_valid != 1:
                response = {
                    'code': 403,
                    'msg': '用户非生效中状态，禁止登录，请联系管理员',
                }
                return (False, response)
            else:
                if server_timestamp < salt_expire_time:
                    password2compare = cf.md5_it(password_without_salt + salt)
                    if password == password2compare:
                        response = {'code': 200, 'msg': '验证成功！', 'user_name': row['name'], 'login_name': row['login_name'], 'user_id': row['id']}
                        return (True, response)
                    else:
                        response = {
                            'code': 403,
                            'msg': '用户名或密码错误！',
                        }
                        return (False, response)
                else:
                    response = {
                        'code': 403,
                        'msg': '时间戳已过期，请刷新页面！',
                    }
                    return (False, response)


@login.route('/userLogin', methods=['POST'])
def userLogin():
    '''
        用户登录逻辑：
            用户表里相关字段有四个：用户密码、固定盐、随机盐、随机盐过期时间
            用户密码存储的是明文密码被MD5加密一次后，再加上固定盐，再MD5加密后的字段
            用户首先调用userLoginGetSalt接口获取固定盐和一个有过期时间的随机盐，随机盐会被存到后端数据库中，有效时间一分钟
            用户前端填写的密码将会MD5加密一次后，加上固定盐再MD5加密一次，再加上随机盐再加密一次，即：md5(md5(md5(password)+stable_salt)+random_salt)
            这样保证了传输过程中是加密的，且每一次传输的都是不一样的字符串
            后端收到用户发来的加密三次的密码后，会使用库里加了固定盐的密码和随机盐相加后MD5，与用户传来的密码相比较，一致则通过
    '''
    login_name = request.get_json()['login_name']
    password = request.get_json()['password']
    is_generate_cookie = request.get_json()['is_generate_cookie']
    login_status, login_response = check_pass(login_name, password)
    if login_status:  # 如果登录成功
        if not is_generate_cookie:  # 如果不需要生成cookie
            return jsonify(login_response)
        else:  # 如果需要生成cookie
            user_key = privilegeFunction().init_user_and_privilege(login_response['user_id'], request.remote_addr)
            login_response['user_key'] = user_key
        return jsonify(login_response)
    else:
        return jsonify(login_response), 500


@login.route('/userLoginSalt', methods=['POST'])
def userLoginSalt():
    try:
        login_name = request.get_json()['login_name']
        salt = cf.random_str(40)
        user_query = user.select().where(user.login_name == login_name).dicts()
        if len(user_query) == 0:
            response = {
                'code': 403,
                'msg': '用户名或密码错误！',
            }
            return jsonify(response), 403
        for row in user_query:
            stable_salt = row['stable_salt']
        user.update(salt=salt, salt_expire_time=(datetime.datetime.now() + datetime.timedelta(minutes=1))).where(user.login_name == login_name).execute()
        return rsp.success({'salt': salt, 'stable_salt': stable_salt})
    except Exception as e:
        return rsp.failed(e), 500


@login.route('/userChangePassword', methods=['POST'])
def userChangePassword():
    try:
        login_name = request.get_json()['login_name']
        user_query = user.select().where(user.login_name == login_name).dicts()
        if len(user_query) == 0:
            response = {
                'code': 403,
                'msg': '用户名或密码错误！',
            }
            return jsonify(response), 403
        else:
            for row in user_query:
                salt_expire_time = row['salt_expire_time']
                server_timestamp = datetime.datetime.now()
                if server_timestamp < salt_expire_time + datetime.timedelta(seconds=ALLOWED_TIME_SPAN):
                    stable_salt = request.get_json()['stable_salt']
                    password = request.get_json()['password']
                    user.update(stable_salt=stable_salt, password=password, update_time=datetime.datetime.now()).where(user.login_name == login_name).execute()
                    pf.del_user_id_to_redis(row['id'])
                    response = {'code': 200, 'msg': '成功'}
                else:
                    response = {'code': 403, 'msg': '登录状态已过期，请返回并重新验证密码'}
        return jsonify(response)
    except Exception as e:
        return rsp.failed(e), 500


@login.route('/userAdd', methods=['POST'])
def userAdd():
    try:
        login_name = request.get_json()['login_name']
        name = request.get_json()['name']
        role_id = request.get_json()['role_id']
        password = request.get_json()['password']
        stable_salt = request.get_json()['stable_salt']
        is_login_name_exist = cf.is_data_existed_in_db(user, user.login_name, login_name)
        if is_login_name_exist:
            response = {'code': 406, 'msg': '已经存在此登录名的用户，请修改您的登录名'}
            return jsonify(response)
        else:
            user.create(
                name=name, login_name=login_name, role_id=role_id, stable_salt=stable_salt, password=password, is_valid=1, create_time=datetime.datetime.now(), update_time=datetime.datetime.now())
            return rsp.success()
    except Exception as e:
        return rsp.failed(e), 500
