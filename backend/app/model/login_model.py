import os
import peewee
import configparser
from peewee import *

cf = configparser.ConfigParser()
cf.read('../homepage.config')
DB_PASS = cf.get('config', 'DB_PASS')


class UnknownField(object):
    def __init__(self, *_, **__):
        pass


class BaseModel(Model):
    class Meta:
        database = MySQLDatabase('my_app', user='root', password=DB_PASS, host='localhost', port=3306)


class user(BaseModel):
    name = CharField()
    login_name = CharField()
    password = CharField()
    stable_salt = CharField()
    salt = CharField()
    salt_expire_time = DateTimeField()
    role_id = IntegerField()
    email = CharField()
    wechat_key = CharField()
    is_valid = IntegerField()
    create_time = DateTimeField()
    update_time = DateTimeField()

    class Meta:
        table_name = 'user'

user.create_table()