import time
import json
import redis
import datetime
import requests
import traceback
import configparser
from . import privilege
from functools import wraps
from flask_cors import cross_origin
from flask import session, redirect, url_for, current_app, flash, Response, request, jsonify, abort
from .model import role, privilege_role
from .model import privilege as privilege_model
from ..common_func import CommonFunc
from ..login.model import user
cf = configparser.ConfigParser()
cf.read('app/homepage.config')
KEY = cf.get('config', 'KEY')

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)


def permission_required(privilege):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_key = request.cookies.get('user_key')
            redis_conn = privilegeFunction().get_redis_conn()

            user_id = redis_conn.get(user_key)

            #是否存在cookie
            if user_id == None:
                abort(403)
                return
            password, ip, random_str, role_id = redis_conn.hmget(user_id, 'password', 'ip', 'random_str', 'role_id')

            #ip是否一致
            if ip != request.remote_addr:
                abort(403)
                return
            user_key_in_redis = CommonFunc().md5_it(random_str + password)

            #cookie是否相同
            if user_key != user_key_in_redis:
                abort(403)
                return

            #是否存在相应权限
            privilege_list = redis_conn.lrange(role_id, 0, -1)
            if privilege not in privilege_list:
                abort(403)
            else:
                return f(*args, **kwargs)

        return decorated_function

    return decorator


class privilegeFunction(object):
    '''
        加密：使用随机字符串+登录用户的密码加密，生成cookie，redis保存cookie、加密后的密码、随机字符串、对应用户id、ip、过期时间，cookie发给客户端后，客户端请求接口要带上cookie
        解密：后端收到cookie后，校验过期时间，如有效则校验ip，如有效则取出cookie对应的加密后的密码、加密时使用的随机字符串，按照加密规则加密后和cookie对比，如果一致，进一步判断权限
        注意：用户修改密码后，应同步处理redis，以使修改密码后cookie失效
    '''
    def __init__(self):
        pass

    def get_redis_conn(self):
        return redis.Redis(connection_pool=pool)

    def set_user_privilege_to_redis(self, user_instance):
        temp = privilegeFunction().get_redis_conn().get(user_instance.role_id)
        if temp == None:
            privilege_role_query = privilege_role.select().where(privilege_role.role_id == user_instance.role_id).dicts()
            for single_privilege_role_query in privilege_role_query:
                self.get_redis_conn().rpush(user_instance.role_id, privilege_model.get(privilege_model.id == single_privilege_role_query['privilege_id']).mark)
        else:
            return

    def set_user_to_redis(self, user_instance, ip):
        random_str = CommonFunc().random_str(40)
        user_key = CommonFunc().md5_it(random_str + user_instance.password)
        self.get_redis_conn().set(user_key, user_instance.id, 36000)
        dict = {'password': user_instance.password, 'ip': ip, 'random_str': random_str, 'role_id': user_instance.role_id}
        self.get_redis_conn().hmset(user_instance.id, dict)
        return user_key

    def init_user_and_privilege(self, user_id, ip):
        user_instance = user.get(user.id == user_id)
        user_key = self.set_user_to_redis(user_instance, ip)
        self.set_user_privilege_to_redis(user_instance)
        return user_key


@privilege.route('/get', methods=['POST'])
@cross_origin()
def get():

    try:
        result = []

        return jsonify({'code': 200, 'msg': '成功！', 'data': result})
    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response)
