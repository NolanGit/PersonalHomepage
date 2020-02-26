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