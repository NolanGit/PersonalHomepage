import os
import peewee
import configparser
from peewee import *
from playhouse.pool import PooledMySQLDatabase
from .model_function import BaseModel




class widget(BaseModel):
    name = CharField()
    is_valid = IntegerField()
    is_login_needed = IntegerField()
    span = IntegerField() # 页面一行的宽度为24
    update_time = DateTimeField()

    class Meta:
        table_name = 'widget'


class widget_user(BaseModel):
    widget_id = IntegerField()
    user_id = IntegerField()
    order = IntegerField()
    is_valid = IntegerField()
    update_time = DateTimeField()

    class Meta:
        table_name = 'widget_user'


widget.create_table()
widget_user.create_table()