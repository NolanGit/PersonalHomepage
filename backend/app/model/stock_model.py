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
        database = PooledMySQLDatabase('PersonalHomepage', user='root', password=DB_PASS, host='localhost', port=3306)


class stock(BaseModel):
    name = CharField()
    code = IntegerField()
    type = IntegerField()
    user_id = IntegerField()
    interval = IntegerField()
    order = IntegerField()
    update_time = DateTimeField()
    is_valid = IntegerField()

    class Meta:
        table_name = 'stock'


class stock_detail(BaseModel):
    price = CharField()
    update_time = DateTimeField()

    class Meta:
        table_name = 'stock_detail'


stock.create_table()
stock_detail.create_table()