import time
import json
import redis
import datetime
import requests
import traceback
from functools import wraps
from flask_cors import cross_origin
from flask import session, redirect, url_for, current_app, flash, Response, request, jsonify, abort
from ..model.login_model import user
from ..model.privilege_model import role, privilege_role
from ..model.privilege_model import privilege as privilege_model
from ..common_func import CommonFunc
from ..response import Response

rsp = Response()
cf = CommonFunc()

pool0 = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True, db=0)
pool1 = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True, db=1)

cf = CommonFunc()
LOGIN_STATUS_EXPIRE_TIME = 36000  # 登录状态在X秒后不活跃则会被置为失效
IS_STATIC_IP = True


# 权限装饰器
def permission_required(privilege):

    def decorator(f):

        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_key = request.cookies.get('user_key')
            pf = privilegeFunction()
            redis_conn = pf.get_redis_conn0()

            # 是否存在cookie
            if user_key == None or redis_conn.exists(user_key) == 0:
                msg = ('[权限校验失败]cookie:%s,URL:%s,原因:不存在cookie' % (user_key, privilege))
                short_msg = '[权限校验失败]登录状态已失效，请刷新页面'
                print(msg)
                return rsp.failed(short_msg), 401

            user_id = redis_conn.get(user_key)
            password, ip, random_str, role_id = redis_conn.hmget(user_id, 'password', 'ip', 'random_str', 'role_id')

            # ip是否一致
            if IS_STATIC_IP:
                if ip != request.remote_addr:
                    msg = ('[权限校验失败]cookie:%s,URL:%s,原因:ip不一致，现ip：%s，允许的ip：%s' % (user_key, privilege, str(ip), str(request.remote_addr)))
                    short_msg = '[权限校验失败]登录状态已失效，请刷新页面'
                    print(msg)
                    return rsp.failed(short_msg), 401
            user_key_in_redis = cf.md5_it(random_str + password)

            # cookie是否相同
            if user_key != user_key_in_redis:
                msg = ('[权限校验失败]cookie:%s,URL:%s,原因:重新加密后的user_key不相同' % (user_key, privilege))
                short_msg = '[权限校验失败]登录状态已失效，请刷新页面'
                print(msg)
                return rsp.failed(short_msg), 401

            # 是否存在角色
            if pf.get_redis_conn1().exists(role_id) == 0:
                msg = ('[权限校验失败]cookie:%s,URL:%s,原因:用户所属角色被删除或禁用' % (user_key, privilege))
                short_msg = '[权限校验失败]用户所属角色被删除或禁用'
                print(msg)
                return rsp.failed(short_msg), 403

            # 是否存在相应权限
            privilege_list = pf.get_redis_conn1().lrange(role_id, 0, -1)
            if privilege not in privilege_list:
                msg = ('[权限校验失败]cookie:%s,URL:%s,原因:不具有权限，用户具有的权限有：%s' % (user_key, privilege, str(privilege_list)))
                short_msg = '[权限校验失败]用户不具有此功能权限'
                print(msg)
                return rsp.failed(short_msg), 403

            # 上述校验均通过，刷新user_key的生效时间，并继续执行业务逻辑
            pf.get_redis_conn0().set(user_key, user_id, LOGIN_STATUS_EXPIRE_TIME)

            return f(*args, **kwargs)

        return decorated_function

    return decorator


# 获取未被删除的用户列表
def user_list_get():
    result = []
    user_query = user.select().where(user.is_valid != -1).order_by(user.id).dicts()
    for row in user_query:
        try:
            update_time = row['update_time'].strftime("%Y-%m-%d %H:%M:%S")
        except:
            update_time = ''
        try:
            create_time = row['create_time'].strftime("%Y-%m-%d %H:%M:%S")
        except:
            create_time = ''
        result.append({
            'id': row['id'],
            'name': row['name'],
            'login_name': row['login_name'],
            'role_id': row['role_id'],
            'is_valid': row['is_valid'],
            'create_time': create_time,
            'update_time': update_time,
        })
    return result


# 获取未被删除的角色
def role_list_get():
    result = []
    role_query = role.select().where(role.is_valid != -1).order_by(role.id).dicts()
    for row in role_query:
        try:
            update_time = row['update_time'].strftime("%Y-%m-%d %H:%M:%S")
        except:
            update_time = ''
        result.append({
            'id': row['id'],
            'name': row['name'],
            'is_valid': row['is_valid'],
            'remark': row['remark'],
            'update_time': update_time,
        })
    return result


# 获取未被删除的权限
def privilege_list_get():
    result = []
    privilege_query = privilege_model.select().where(privilege_model.is_valid != -1).order_by(privilege_model.id).dicts()
    for row in privilege_query:
        try:
            update_time = row['update_time'].strftime("%Y-%m-%d %H:%M:%S")
        except:
            update_time = ''
        result.append({'id': row['id'], 'name': row['name'], 'mark': row['mark'], 'remark': row['remark'], 'is_valid': row['is_valid'], 'update_time': update_time})
    return result


# 获取有效的角色权限对应关系
def privilege_role_list_get():
    result = []
    privilege_role_query = privilege_role.select().where(privilege_role.is_valid == 1).order_by(privilege_role.id).dicts()
    for row in privilege_role_query:
        result.append({
            'id': row['id'],
            'privilege_id': row['privilege_id'],
            'role_id': row['role_id'],
        })
    return result


# 权限相关方法
class privilegeFunction(object):

    '''
        加密：使用随机字符串+登录用户的密码加密，生成cookie，redis保存cookie和用户id的对应关系，用户id和加密后的密码、随机字符串、对应用户id、ip、登录时间的对应哈希，cookie发给客户端后，客户端请求接口要带上cookie
        解密：后端收到cookie后，校验是否存在cookide(是否过期)，如有效则取出用户id后校验ip，如有效则取出cookie对应的加密后的密码、加密时使用的随机字符串，按照加密规则加密后和cookie对比，如果一致，进一步判断权限
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

    def flush_role_privilege_to_redis(self, role_id):
        '''
            更新角色的权限列表到redis
            args : role_id(Int)
        '''
        print('刷新角色id为[%s]具有的权限列表' % role_id)

        IS_ROLE_ID_VALID = False if role.get(role.id == role_id).is_valid != 1 else True  # 权限id是否有效
        IS_ROLE_ID_IN_REDIS = False if privilegeFunction().get_redis_conn1().exists(role_id) == 0 else True  # redis中是否有该权限id的数据

        if IS_ROLE_ID_VALID:
            if IS_ROLE_ID_IN_REDIS:
                '''
                    如果redis中有该权限id的数据，则需要清空后刷入新的
                '''
                print('检测到存在角色id为[%s]的缓存，即将删除' % role_id)
                privilegeFunction().get_redis_conn1().delete(role_id)
                self.flush_role_privilege_to_redis(role_id)
            else:
                '''
                    如果redis中没有该权限id的数据，则刷入权限。首先取出用户的角色具有的的权限，如果该权限为有效状态，则添加
                '''
                privilege_role_query = privilege_role.select().where((privilege_role.role_id == role_id) & (privilege_role.is_valid == 1)).dicts()
                for single_privilege_role_query in privilege_role_query:
                    privilege_to_be_added = privilege_model.get(privilege_model.id == single_privilege_role_query['privilege_id'])
                    if privilege_to_be_added.is_valid == 1:
                        self.get_redis_conn1().rpush(role_id, privilege_to_be_added.mark)
        else:
            if IS_ROLE_ID_IN_REDIS:
                privilegeFunction().get_redis_conn1().delete(role_id)
            else:
                return

    def flush_privilege_which_belongs_to_role_with_target_privilege_to_redis(self, privilege_id):
        '''
            接受一个权限id，刷新所有具有此权限的角色的拥有的权限列表到redis
            args : privilege_id(Int)
        '''
        privilege_role_list = privilege_role_list_get()
        affected_role_id_set = set(cf.dict_list_get_all_element(privilege_role_list, 'privilege_id', privilege_id, 'role_id'))
        print('修改权限id[%s]被影响的角色id有%s' % (privilege_id, str(affected_role_id_set)))
        for affected_role_id in affected_role_id_set:
            self.flush_role_privilege_to_redis(affected_role_id)

    def set_user_to_redis(self, user_instance, ip):
        '''
            存用户相关信息到redis，返回一个加密串
            args : user_instance(User), ip(String)
            return : user_key(String)
        '''
        random_str = cf.random_str(40)
        user_key = cf.md5_it(random_str + user_instance.password)
        self.get_redis_conn0().set(user_key, user_instance.id, LOGIN_STATUS_EXPIRE_TIME)
        dict = {'password': user_instance.password, 'ip': ip, 'random_str': random_str, 'role_id': user_instance.role_id, 'login_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        self.get_redis_conn0().hmset(user_instance.id, dict)
        return user_key

    def del_user_key_to_redis(self, user_key):
        self.get_redis_conn0().delete(user_key)

    def del_user_id_to_redis(self, user_id):
        self.get_redis_conn0().delete(user_id)

    def del_role_to_redis(self, role_id):
        self.get_redis_conn1().delete(role_id)

    def init_user_and_privilege(self, user_id, ip):
        user_instance = user.get(user.id == user_id)
        user_key = self.set_user_to_redis(user_instance, ip)
        self.flush_role_privilege_to_redis(user_instance.role_id)
        return user_key
