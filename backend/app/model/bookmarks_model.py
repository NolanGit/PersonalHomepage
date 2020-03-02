import os
import peewee
import configparser
from peewee import *
from playhouse.pool import PooledMySQLDatabase

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))
cf = configparser.ConfigParser()
cf.read(PATH('../homepage.config'))
DB_PASS = cf.get('config', 'DB_PASS')


class UnknownField(object):

    def __init__(self, *_, **__):
        pass


class BaseModel(Model):

    class Meta:
        database = PooledMySQLDatabase('my_app', user='root', password=DB_PASS, host='localhost', port=3306)



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