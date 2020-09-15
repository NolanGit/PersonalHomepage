import os
import peewee
from peewee import CharField, IntegerField, DateTimeField
from .model_function import BaseModel


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