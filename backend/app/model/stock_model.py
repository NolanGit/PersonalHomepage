import os
import peewee
import configparser
from peewee import *
from playhouse.pool import PooledMySQLDatabase
from model_function import BaseModel


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