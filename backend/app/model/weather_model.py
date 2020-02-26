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


class weather_personalized(BaseModel):
    location = CharField()
    user_id = IntegerField()
    is_valid = IntegerField()
    update_time = DateTimeField()

    class Meta:
        table_name = 'weather_personalized'

weather_personalized.create_table()