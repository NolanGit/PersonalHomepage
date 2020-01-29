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


# 权限装饰器
def permission_required(privilege):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_key = request.cookies.get('user_key')
            redis_conn = privilegeFunction().get_redis_conn0()

            #是否存在cookie
            if user_key == None or redis_conn.exists(user_key) == 0:
                msg = ('[权限校验失败]cookie:%s,URL:%s,原因:不存在cookie' % (user_key, privilege))
                print(msg)
                response = {'code': 403, 'message': msg}
                return jsonify(response), 403

            user_id = redis_conn.get(user_key)
            password, ip, random_str, role_id = redis_conn.hmget(user_id, 'password', 'ip', 'random_str', 'role_id')

            #ip是否一致
            if ip != request.remote_addr:
                msg = ('[权限校验失败]cookie:%s,URL:%s,原因:ip不一致，现ip：%s，允许的ip：%s' % (user_key, privilege, str(ip), str(request.remote_addr)))
                print(msg)
                response = {'code': 403, 'message': msg}
                return jsonify(response), 403
            user_key_in_redis = cf.md5_it(random_str + password)

            #cookie是否相同
            if user_key != user_key_in_redis:
                msg = ('[权限校验失败]cookie:%s,URL:%s,原因:重新加密后的user_key不相同' % (user_key, privilege))
                print(msg)
                response = {'code': 403, 'message': msg}
                return jsonify(response), 403

            #是否存在角色
            if privilegeFunction().get_redis_conn1().exists(role_id) == 0:
                msg = ('[权限校验失败]cookie:%s,URL:%s,原因:用户所属角色被删除或禁用' % (user_key, privilege))
                print(msg)
                response = {'code': 403, 'message': msg}
                return jsonify(response), 403

            #是否存在相应权限
            privilege_list = privilegeFunction().get_redis_conn1().lrange(role_id, 0, -1)
            if privilege not in privilege_list:
                msg = ('[权限校验失败]cookie:%s,URL:%s,原因:不具有权限，用户具有的权限有：%s' % (user_key, privilege, str(privilege_list)))
                print(msg)
                response = {'code': 403, 'message': msg}
                return jsonify(response), 403
            else:
                return f(*args, **kwargs)

        return decorated_function

    return decorator


# 权限相关方法
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

    def flush_user_privilege_to_redis(self, role_id):
        '''
            存用户的权限列表到redis
            args : role_id(Int)
        '''
        is_valid = role.get(role.id == role_id).is_valid
        if is_valid == 0:
            return
        temp = privilegeFunction().get_redis_conn1().exists(role_id)
        if temp == 0:
            privilege_role_query = privilege_role.select().where((privilege_role.role_id == role_id) & (privilege_role.is_valid == 1)).dicts()
            for single_privilege_role_query in privilege_role_query:
                self.get_redis_conn1().rpush(role_id, privilege_model.get(privilege_model.id == single_privilege_role_query['privilege_id']).mark)
        else:
            privilegeFunction().get_redis_conn1().delete(role_id)
            self.flush_user_privilege_to_redis(role_id)

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

    def del_user_to_redis(self, user_key):
        self.get_redis_conn0().delete(user_key)

    def del_role_to_redis(self, role_id):
        self.get_redis_conn1().delete(role_id)

    def init_user_and_privilege(self, user_id, ip):
        user_instance = user.get(user.id == user_id)
        user_key = self.set_user_to_redis(user_instance, ip)
        self.flush_user_privilege_to_redis(user_instance.role_id)
        return user_key


# 获取生效中的用户列表
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


# 获取未被删除的角色
def role_list_get():
    result = []
    role_query = role.select().where(role.is_valid != -1).order_by(role.id).dicts()
    for row in role_query:
        result.append({
            'id': row['id'],
            'name': row['name'],
            'is_valid': row['is_valid'],
            'remark': row['remark'],
            'update_time': row['update_time'],
        })
    return result


# 获取未被删除的权限
def privilege_list_get():
    result = []
    privilege_query = privilege_model.select().where(role.is_valid != -1).order_by(privilege_model.id).dicts()
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


# 用户列表获取（带有用户的角色信息）
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


# 用户信息修改
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


# 角色列表获取
@privilege.route('/roleGet', methods=['GET'])
@cross_origin()
def roleGet():
    try:
        return jsonify({'code': 200, 'msg': '成功！', 'data': role_list_get()})
    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response)


# 角色具有的权限列表获取
@privilege.route('/rolePrivilegeGet', methods=['POST'])
@cross_origin()
def rolePrivilegeGet():
    try:
        role_id = request.get_json()['role_id']
        result = []
        privilege_list = privilege_list_get()
        privilege_role_query = privilege_role.select().where((privilege_role.role_id == role_id) & (privilege_role.is_valid == 1)).order_by(privilege_role.id).dicts()
        for row in privilege_role_query:
            result.append({
                'privilege_id': row['privilege_id'],
                'privilege_name': cf.dict_list_get_element(privilege_list, 'id', row['privilege_id'], 'name', row['privilege_id'] - 1),
            })
        return jsonify({'code': 200, 'msg': '成功！', 'data': result})
    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response)


# 角色对应权限修改
@privilege.route('/rolePrivilegeEdit', methods=['POST'])
@cross_origin()
def rolePrivilegeEdit():
    try:
        role_id = request.get_json()['role_id']
        checked_privilege_id = request.get_json()['checked_privilege_id']
        privilege_role.update(is_valid=0).where(privilege_role.role_id == role_id).execute()
        data_source = []
        for single_checked_privilege_id in checked_privilege_id:
            data_source.append((single_checked_privilege_id, role_id, 1))
        field = [privilege_role.privilege_id, privilege_role.role_id, privilege_role.is_valid]
        privilege_role.insert_many(data_source, field).execute()
        privilegeFunction().flush_user_privilege_to_redis(role_id)
        response = {'code': 200, 'msg': '成功'}
        return jsonify(response)
    except Exception as e:
        response = {'code': 500, 'msg': e, 'data': {}}
        return jsonify(response)


# 角色信息新增和修改
@privilege.route('/roleEdit', methods=['POST'])
@cross_origin()
def roleEdit():
    try:
        role_id = request.get_json()['role_id']
        name = request.get_json()['name']
        remark = request.get_json()['remark']
        if role_id == 0:
            role.create(name=name, remark=remark, is_valid=1, update_time=datetime.datetime.now())
        else:
            role.update(name=name, remark=remark, is_valid=1, update_time=datetime.datetime.now()).where(role.id == role_id).execute()
        return jsonify({'code': 200, 'msg': '成功！'})
    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response)


# 角色禁用
@privilege.route('/roleDisable', methods=['POST'])
@cross_origin()
def roleDisable():
    try:
        role_id = request.get_json()['role_id']
        role.update(is_valid=0, update_time=datetime.datetime.now()).where(role.id == role_id).execute()
        privilegeFunction().del_role_to_redis(role_id)
        return jsonify({'code': 200, 'msg': '成功！'})
    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response)


# 角色启用
@privilege.route('/roleAble', methods=['POST'])
@cross_origin()
def roleAble():
    try:
        role_id = request.get_json()['role_id']
        role.update(is_valid=1, update_time=datetime.datetime.now()).where(role.id == role_id).execute()
        privilegeFunction().flush_user_privilege_to_redis(role_id)
        return jsonify({'code': 200, 'msg': '成功！'})
    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response)


# 角色删除
@privilege.route('/roleDelete', methods=['POST'])
@cross_origin()
def roleDelete():
    try:
        role_id = request.get_json()['role_id']
        role.update(is_valid=-1, update_time=datetime.datetime.now()).where(role.id == role_id).execute()
        privilegeFunction().del_role_to_redis(role_id)
        return jsonify({'code': 200, 'msg': '成功！'})
    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response)


#权限列表获取
@privilege.route('/privilegeGet', methods=['GET'])
@cross_origin()
def privilegeGet():
    try:
        return jsonify({'code': 200, 'msg': '成功！', 'data': privilege_list_get()})
    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response)


#权限新增和修改
@privilege.route('/privilegeEdit', methods=['POST'])
@cross_origin()
def privilegeEdit():
    try:
        privilege_id = request.get_json()['privilege_id']
        name = request.get_json()['name']
        mark = request.get_json()['mark']
        remark = request.get_json()['remark']
        if privilege_id == 0:
            privilege_model.create(name=name, mark=mark, remark=remark, is_valid=1, update_time=datetime.datetime.now())
        else:
            privilege_model.update(name=name, mark=mark, remark=remark, is_valid=1, update_time=datetime.datetime.now()).where(privilege_model.id == privilege_id).execute()
        return jsonify({'code': 200, 'msg': '成功！'})
    except Exception as e:
        traceback.print_exc()
        response = {'code': 500, 'msg': '失败！错误信息：' + str(e) + '，请联系管理员。', 'data': []}
        return jsonify(response)
