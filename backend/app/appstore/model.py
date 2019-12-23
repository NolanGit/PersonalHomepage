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
    is_valid = IntegerField()
    notify = IntegerField() # 1:是,2:否
    notify_method = IntegerField() # 1:微信,2:邮件
    notify_time = DateTimeField()
    notify_interval = IntegerField()
    notify_interval_unit = IntegerField() # 1:小时,2:天
    notify_trigger_time = DateTimeField()
    update_time = DateTimeField()

    class Meta:
        table_name = 'appstore'

#用户表增加email和微信推送id的config

class appstore_price_data(BaseModel):
    app_id = IntegerField()
    crawling_times = IntegerField()
    time = TimeField()
    date = DateField()

    class Meta:
        table_name = 'appstore_price_data'

appstore.create_table()
appstore_price_data.create_table()