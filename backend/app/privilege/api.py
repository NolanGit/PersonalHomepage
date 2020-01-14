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
cf = configparser.ConfigParser()
cf.read('app/homepage.config')
KEY = cf.get('config', 'KEY')


def privilege_flush(User):
    pass


def permission_required(privellge):
    print(privellge)
    def decorator(f):

        @wraps(f)
        def decorated_function(*args, **kwargs):
            print(privilege)
            user_key = request.cookies.get('user_key')
            privilege_list = privilegeFunction().privellge_get(user_key)
            print(privilege_list)
            if privilege in privilege_list:
                return f(*args, **kwargs)
            else:
                abort(403)

        return decorated_function

    return decorator


class privilegeFunction(object):

    def __init__(self):
        pool = redis.ConnectionPool(host='localhost', port=6379, db=1)
        self.pool = pool

    def get_redis_conn(self):
        return redis.Redis(connection_pool=self.pool)

    def set_user_privilege_to_redis(self, user_role_id, privilege_key):
        privilege_role_query = privilege_role.select().where(privilege_role.role_id == user_role_id).dicts()
        for single_privilege_role_query in privilege_role_query:
            self.get_redis_conn().rpush(privilege_key, privilege_model.get(privilege_model.id == single_privilege_role_query['privilege_id']).mark)

    def set_user_to_redis(self, user_id):
        user_key = CommonFunc().random_str(40)
        privilege_key = CommonFunc().random_str(40)
        user_dict = {'user_id': user_id, 'privilege_key': privilege_key}
        self.get_redis_conn().hmset(user_key, user_dict)
        return user_key, privilege_key

    def init_user_and_privilege(self, user_id, user_role_id):
        user_key, privilege_key = self.set_user_to_redis(user_id)
        self.set_user_privilege_to_redis(user_role_id, privilege_key)
        return user_key

    def privellge_get(self, user_key):
        privilege_key = self.get_redis_conn().hget(user_key, "privilege_key")
        return self.get_redis_conn().lrange(privilege_key, 0, -1)

    def user_id_get(self, user_key):
        return self.get_redis_conn().hget(user_key, "user_id")

    def permission_required(self, privellge):

        def decorator(f):

            @wraps(f)
            def decorated_function(*args, **kwargs):
                print(privilege)
                user_key = request.cookies.get('user_key')
                privilege_list = self.privellge_get(user_key)
                print(privilege_list)
                if privilege in privilege_list:
                    return f(*args, **kwargs)
                else:
                    abort(403)

            return decorated_function

        return decorator


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
