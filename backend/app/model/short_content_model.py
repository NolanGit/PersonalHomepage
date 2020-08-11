import os
import peewee
from peewee import CharField, IntegerField, DateTimeField
from .model_function import BaseModel


class short_content(BaseModel):
    code = CharField()
    content = CharField()
    type = IntegerField()  # 1:URL
    is_valid = IntegerField()
    expire_time = DateTimeField()
    update_time = DateTimeField()

    class Meta:
        table_name = 'short_content'


short_content.create_table()