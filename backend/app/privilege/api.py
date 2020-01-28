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
                msg = ('[使用cookie"%s"访问%s权限校验失败]不存在cookie' % (user_key, privilege))
                print(msg)
                abort(403)
                response = {'code': 403, 'msg': msg}
                return jsonify(response)

            user_id = redis_conn.get(user_key)
            password, ip, random_str, role_id = redis_conn.hmget(user_id, 'password', 'ip', 'random_str', 'role_id')

            #ip是否一致
            if ip != request.remote_addr:
                msg = ('[使用cookie"%s"访问%s权限校验失败]ip不一致，现ip：%s，允许的ip：%s' % (user_key, privilege, str(ip), str(request.remote_addr)))
                print(msg)
                abort(403)
                response = {'code': 403, 'msg': msg}
                return jsonify(response)
            user_key_in_redis = cf.md5_it(random_str + password)

            #cookie是否相同
            if user_key != user_key_in_redis:
                msg = ('[使用cookie"%s"访问%s权限校验失败]重新加密后的user_key不相同' % (user_key, privilege))
                print(msg)
                abort(403)
                response = {'code': 403, 'msg': msg}
                return jsonify(response)

            #是否存在相应权限
            privilege_list = privilegeFunction().get_redis_conn1().lrange(role_id, 0, -1)
            if privilege not in privilege_list:
                msg = ('[使用cookie"%s"访问%s权限校验失败]不具有权限，用户具有的权限有：%s' % (user_key, privilege, str(privilege_list)))
                print(msg)
                abort(403)
                response = {'code': 403, 'msg': msg}
                return jsonify(response)
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
            'is_valid': row['is_valid'],
            'remark': row['remark'],
            'update_time': row['update_time'],
        })
    return result


def user_list_get():
    result = []
    user_query = user.select().where(user.is_valid == 1).order_by(user.id).dicts()
    for row in user_query:
        result.append({
            'id': row['id'],
            'name': row['name'],
            'login_name': row['login_name'],
            'role_id': row['role_id'],
            'create_time': row['create_time'],
            'update_time': row['update_time'],
        })
    return result


def privilege_list_get():
    result = []
    privilege_query = privilege_model.select().order_by(privilege_model.id).dicts()
    for row in privilege_query:
        result.append({
            'id': row['id'],
            'name': row['name'],
            'mark': row['mark'],
            'remark': row['remark'],
            'is_valid': row['is_valid'],
            'update_time': row['update_time'],
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
        if temp == 0:
            privilege_role_query = privilege_role.select().where(privilege_role.role_id == user_instance.role_id).dicts()
            for single_privilege_role_query in privilege_role_query:
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
        return jsonify({'code': 200, 'msg': '成功！', 'data': privilege_list_get()})
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
        current_role_id = cf.dict_list_get_element(user_list, 'name', user_name, 'role_id')
        current_user_role = cf.dict_list_get_element(role_list, 'id', current_role_id, 'name', current_role_id - 1)
        if current_user_role == '管理员':
            for single_user in user_list:
                single_user['is_edit'] = 1
                single_user['role_name'] = cf.dict_list_get_element(role_list, 'id', single_user['role_id'], 'name', single_user['role_id'] - 1)
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


@privilege.route('/rolePrivilegeGet', methods=['POST'])
@cross_origin()
def rolePrivilegeGet():
    try:
        role_id = request.get_json()['role_id']
        result = []
        # privilege_list = privilege_list_get()
        privilege_role_query = privilege_role.select().where(privilege_role.role_id == role_id).order_by(privilege_role.id).dicts()
        for row in privilege_role_query:
            result.append({
                'privilege_id': row['privilege_id'],
                # 'privilege_name': cf.dict_list_get_element(privilege_list, 'id', row['privilege_id'], 'mark', row['privilege_id'] - 1),
            })
        return jsonify({'code': 200, 'msg': '成功！', 'data': result})
    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response)


@privilege.route('/userRoleChange', methods=['POST'])
@cross_origin()
def userRoleChange():
    ALLOWED_TIME_SPAN = 100  # 盐过期X秒内允许修改，否则需要重新登录
    try:
        login_name = request.get_json()['login_name']
        user_query = user.select().where(user.login_name == login_name).dicts()
        if len(user_query) == 0:
            response = {
                'code': 403,
                'msg': '用户名或密码错误！',
            }
            return (False, response)
        else:
            for row in user_query:
                salt_expire_time = row['salt_expire_time']
                server_timestamp = int(time.mktime(datetime.datetime.now().timetuple()))
                if server_timestamp < salt_expire_time + ALLOWED_TIME_SPAN:
                    role_id = request.get_json()['role_id']
                    user.update(role_id=role_id, update_time=datetime.datetime.now()).where(user.login_name == login_name).execute()
                    response = {'code': 200, 'msg': '成功'}
                else:
                    response = {'code': 403, 'msg': '登录状态已过期，请返回并重新验证密码'}
        return jsonify(response)
    except Exception as e:
        response = {'code': 500, 'msg': e, 'data': {}}
        return jsonify(response)