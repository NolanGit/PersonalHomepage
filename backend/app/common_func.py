import redis
from functools import wraps
from .login.model import user
from flask import request, jsonify
from .search.model import search_engines


class CommonFunc(object):
    def get_search_engine_id(self, search_engine_name):
        search_engines_query = search_engines.select().where(search_engines.name == search_engine_name).limit(1).dicts()
        if len(search_engines_query) == 0:
            return None
        else:
            for row in search_engines_query:
                return row['id']


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


class RedisClass(object):

    pool = redis.ConnectionPool(host='localhost', port=6379, db=1)

    def __init__(self, pool):
        self.pool = pool


def permission_required(privellge):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            request.get_json()['sub_system_id']
            print(request.get_json()['sub_system_id'])
            print(privellge)
            return f(*args, **kwargs)

        return decorated_function

    return decorator