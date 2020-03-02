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


class icon(BaseModel):
    name = CharField()

    class Meta:
        table_name = 'icon'


class bookmarks(BaseModel):
    name = CharField()
    url = CharField()
    icon = CharField()
    order = IntegerField()
    user_id = IntegerField()
    is_valid = IntegerField()
    update_time = DateTimeField()

    class Meta:
        table_name = 'bookmarks'


bookmarks.create_table()