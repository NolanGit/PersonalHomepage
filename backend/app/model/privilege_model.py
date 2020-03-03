import os
import peewee
import configparser
from peewee import *
from playhouse.pool import PooledMySQLDatabase
from model_function import BaseModel

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