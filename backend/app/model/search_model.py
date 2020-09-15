import os
import peewee
from peewee import CharField, IntegerField, DateTimeField
from .model_function import BaseModel


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
    engine_id = IntegerField()
    search_text = CharField()
    ip = CharField()
    update_time = DateTimeField()

    class Meta:
        table_name = 'search_engines_log'


search_engines.create_table()
search_engines_log.create_table()