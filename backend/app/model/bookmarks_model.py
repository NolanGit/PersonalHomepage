import os
import peewee
from peewee import CharField, IntegerField, DateTimeField
from .model_function import BaseModel


class icon(BaseModel):
    name = CharField()
    category = IntegerField()

    class Meta:
        table_name = 'icon'

class icon_category(BaseModel):
    name = CharField()

    class Meta:
        table_name = 'icon_category'

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
icon_category.create_table()
bookmarks.create_table()