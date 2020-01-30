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


class search_engines(BaseModel):
    name = CharField()
    main_url = CharField()
    auto_complete_url = CharField()
    icon = CharField()

    class Meta:
        table_name = 'search_engines'

class search_engines_log(BaseModel):
    user_id = IntegerField()
    user = CharField()
    engine_id= IntegerField()
    search_text = CharField()
    ip = CharField()
    update_time = DateTimeField()

    class Meta:
        table_name = 'search_engines_log'

search_engines.create_table()
search_engines_log.create_table()