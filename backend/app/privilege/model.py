import os
import peewee
from peewee import *

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))
database = peewee.SqliteDatabase(PATH("../../data.sqlite"))


class UnknownField(object):
    def __init__(self, *_, **__):
        pass


class BaseModel(Model):
    class Meta:
        database = database


class role(BaseModel):
    name = CharField()
    remark = CharField(null=True)
    update_time = DateTimeField(null=True)

    class Meta:
        table_name = 'role'

class privilege(BaseModel):
    name = CharField()
    mark = CharField()
    remark = CharField(null=True)
    update_time = DateTimeField(null=True)

    class Meta:
        table_name = 'privilege'

class privilege_role(BaseModel):
    privilege_id = IntegerField()
    role_id = IntegerField()

    class Meta:
        table_name = 'privilege_role'

role.create_table()
privilege.create_table()
privilege_role.create_table()