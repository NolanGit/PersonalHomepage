import os
import peewee
import configparser
from peewee import *

cf = configparser.ConfigParser()
cf.read('../homepage.config')


class UnknownField(object):
    def __init__(self, *_, **__):
        pass


class BaseModel(Model):
    class Meta:
        database = MySQLDatabase('my_app', user='root', password=cf.get('config', 'DB_PASS'), host='localhost', port=3306)


class role(BaseModel):
    name = CharField()
    remark = CharField(null=True)
    is_valid = IntegerField()
    update_time = DateTimeField(null=True)

    class Meta:
        table_name = 'role'

class privilege(BaseModel):
    name = CharField()
    mark = CharField()
    remark = CharField(null=True)
    is_valid = IntegerField()
    update_time = DateTimeField(null=True)

    class Meta:
        table_name = 'privilege'

class privilege_role(BaseModel):
    privilege_id = IntegerField()
    role_id = IntegerField()
    is_valid = IntegerField()

    class Meta:
        table_name = 'privilege_role'

role.create_table()
privilege.create_table()
privilege_role.create_table()