import os
import peewee
from peewee import CharField, IntegerField, DateTimeField
from .model_function import BaseModel


class image(BaseModel):
    file_name = CharField()
    file_path = CharField()
    token = CharField()
    user_id = IntegerField()
    update_time = DateTimeField()

    class Meta:
        table_name = 'image'


image.create_table()