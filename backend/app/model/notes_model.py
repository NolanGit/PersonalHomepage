import os
import peewee
from peewee import CharField, IntegerField, DateTimeField
from .model_function import BaseModel


class notes(BaseModel):
    name = CharField()
    content = CharField()
    user_id = IntegerField()
    is_valid = IntegerField()
    update_time = DateTimeField()

    class Meta:
        table_name = 'notes'

notes.create_table()