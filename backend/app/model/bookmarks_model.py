import os
import peewee
import configparser
from peewee import *
from .model_function import BaseModel


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


icon.create_table()
bookmarks.create_table()