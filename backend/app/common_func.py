import redis
from functools import wraps
from .login.model import user
from flask import request, jsonify
from .search.model import search_engines
import random
import hashlib


class CommonFunc(object):

    def get_search_engine_id(self, search_engine_name):
        search_engines_query = search_engines.select().where(search_engines.name == search_engine_name).limit(1).dicts()
        if len(search_engines_query) == 0:
            return None
        else:
            for row in search_engines_query:
                return row['id']

    def random_str(self, num):
        H = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

        salt = ''
        for i in range(num):
            salt += random.choice(H)

        return salt

    def md5_it(self, str):
        str_md5 = hashlib.md5(str.encode('utf-8')).hexdigest()
        return str_md5


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
