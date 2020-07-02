import os
import peewee
from peewee import *
from .model_function import BaseModel


class upload(BaseModel):
    file_name = CharField()
    file_path = CharField()
    user_id = IntegerField()
    update_time = DateTimeField()

    class Meta:
        table_name = 'upload'


upload.create_table()