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


class appstore(BaseModel):
    name = CharField()
    url = CharField()
    expect_price = IntegerField()
    user_id = IntegerField()
    order = IntegerField()
    is_notify = IntegerField()
    is_valid = IntegerField()
    update_time = DateTimeField()

    class Meta:
        table_name = 'appstore'

#用户表增加email

class appstore_price_data(BaseModel):
    app_id = IntegerField()
    crawling_times = IntegerField()
    time = TimeField()
    date = DateField()

    class Meta:
        table_name = 'appstore_price_data'

appstore.create_table()
appstore_price_data.create_table()