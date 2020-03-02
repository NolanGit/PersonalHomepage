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