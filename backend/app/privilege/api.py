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

pool0 = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True, db=0)
pool1 = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True, db=1)
cf = CommonFunc()


def permission_required(privilege):

    def decorator(f):

        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_key = request.cookies.get('user_key')
            redis_conn = privilegeFunction().get_redis_conn0()

            #是否存在cookie
            if user_key == None or redis_conn.exists(user_key) == 0:
                abort(403)
                return
            user_id = redis_conn.get(user_key)
            password, ip, random_str, role_id = redis_conn.hmget(user_id, 'password', 'ip', 'random_str', 'role_id')

            #ip是否一致
            if ip != request.remote_addr:
                abort(403)
                return
            user_key_in_redis = cf.md5_it(random_str + password)

            #cookie是否相同
            if user_key != user_key_in_redis:
                abort(403)
                return

            #是否存在相应权限
            privilege_list = privilegeFunction().get_redis_conn1().lrange(role_id, 0, -1)
            if privilege not in privilege_list:
                abort(403)
            else:
                return f(*args, **kwargs)

        return decorated_function

    return decorator


def role_list_get():
    result = []
    role_query = role.select().where(role.is_valid == 1).order_by(role.id).dicts()
    for row in role_query:
        result.append({
            'id': row['id'],
            'name': row['name'],
            'remark': row['remark'],
        })
    return result


def user_list_get():
    result = []
    user_query = user.select().where(user.is_valid == 1).order_by(user.id).dicts()
    for row in user_query:
        result.append({
            'id': row['id'],
            'name': row['name'],
            'role_id': row['role_id'],
            'create_time': row['create_time'],
        })
    return result


class privilegeFunction(object):

    '''
        加密：使用随机字符串+登录用户的密码加密，生成cookie，redis保存cookie、加密后的密码、随机字符串、对应用户id、ip、过期时间，cookie发给客户端后，客户端请求接口要带上cookie
        解密：后端收到cookie后，校验过期时间，如有效则校验ip，如有效则取出cookie对应的加密后的密码、加密时使用的随机字符串，按照加密规则加密后和cookie对比，如果一致，进一步判断权限
        注意：用户修改密码后，应同步处理redis，以使修改密码后cookie失效
    '''

    def __init__(self):
        pass

    def get_redis_conn0(self):
        #获取redis连接
        return redis.Redis(connection_pool=pool0)

    def get_redis_conn1(self):
        #获取redis连接
        return redis.Redis(connection_pool=pool1)

    def flush_user_privilege_to_redis(self, user_instance):
        '''
            存用户的权限列表到redis
            args : user_instance(User)
        '''
        temp = privilegeFunction().get_redis_conn1().exists(user_instance.role_id)
        print(temp)
        if temp == 0:
            privilege_role_query = privilege_role.select().where(privilege_role.role_id == user_instance.role_id).dicts()
            for single_privilege_role_query in privilege_role_query:
                print(privilege_model.get(privilege_model.id == single_privilege_role_query['privilege_id']).mark)
                self.get_redis_conn1().rpush(user_instance.role_id, privilege_model.get(privilege_model.id == single_privilege_role_query['privilege_id']).mark)
        else:
            privilegeFunction().get_redis_conn1().delete(user_instance.role_id)
            self.flush_user_privilege_to_redis(user_instance)

    def set_user_to_redis(self, user_instance, ip):
        '''
            存用户相关信息到redis，返回一个加密串
            args : user_instance(User), ip(String)
            return : user_key(String)
        '''
        random_str = cf.random_str(40)
        user_key = cf.md5_it(random_str + user_instance.password)
        self.get_redis_conn0().set(user_key, user_instance.id, 36000)
        dict = {'password': user_instance.password, 'ip': ip, 'random_str': random_str, 'role_id': user_instance.role_id}
        self.get_redis_conn0().hmset(user_instance.id, dict)
        return user_key

    def del_user_to_redis(self, db, user_key):
        self.get_redis_conn0().delete(user_key)

    def init_user_and_privilege(self, user_id, ip):
        user_instance = user.get(user.id == user_id)
        user_key = self.set_user_to_redis(user_instance, ip)
        self.flush_user_privilege_to_redis(user_instance)
        return user_key


@privilege.route('/privilegeGet', methods=['GET'])
@cross_origin()
def get():

    try:
        result = []
        privilege_model_query = privilege_model.select().where(privilege_model.is_valid == 1).dicts()
        for row in privilege_model_query:
            result.append({
                'id': row['id'],
                'name': row['name'],
                'mark': row['mark'],
                'remark': row['remark'],
                'update_time': row['update_time'],
            })
        return jsonify({'code': 200, 'msg': '成功！', 'data': result})
    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response)


@privilege.route('/userGet', methods=['POST'])
@cross_origin()
def userGet():

    try:
        user_name = request.get_json()['user']
        result = []
        role_list = role_list_get()
        user_list = user_list_get()
        print(user_list)
        current_role_id = cf.dict_list_get_element(user_list, 'name', user_name, 'role_id')
        current_user_role = cf.dict_list_get_element(role_list, 'id', current_role_id, 'name', current_role_id - 1)
        if current_user_role == '管理员':
            for single_user in user_list:
                single_user['is_edit'] = 1
                single_user['role_name'] = cf.dict_list_get_element(role_list, 'id', single_user['role_id'], 'name', single_user['role_id'])
        else:
            for single_user in user_list:
                if single_user['name'] == user_name:
                    single_user['is_edit'] = 1
                else:
                    single_user['is_edit'] = 0
        return jsonify({'code': 200, 'msg': '成功！', 'data': user_list})
    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response)


@privilege.route('/roleGet', methods=['GET'])
@cross_origin()
def roleGet():

    try:
        return jsonify({'code': 200, 'msg': '成功！', 'data': role_list_get()})
    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response)
