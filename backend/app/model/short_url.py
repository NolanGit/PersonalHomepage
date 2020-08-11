import os
import peewee
from peewee import CharField, IntegerField, DateTimeField
from .model_function import BaseModel


class short_url(BaseModel):
    code = CharField()
    content = CharField()
    type = IntegerField()
    is_valid = IntegerField()
    expire_time = DateTimeField()
    update_time = DateTimeField()

    class Meta:
        table_name = 'short_url'


short_url.create_table()