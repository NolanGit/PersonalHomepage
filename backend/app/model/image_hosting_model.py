import os
import peewee
from peewee import CharField, IntegerField, DateTimeField
from .model_function import BaseModel


class image_hosting(BaseModel):
    file_name = CharField()
    file_path = CharField()
    token = CharField()
    user_id = IntegerField()
    is_valid = IntegerField()
    update_time = DateTimeField()

    class Meta:
        table_name = 'image_hosting'


image_hosting.create_table()