import os
import peewee
from peewee import CharField, DateTimeField
from .model_function import BaseModel


class ip_location(BaseModel):
    ip = CharField()
    location = CharField()
    update_time = DateTimeField()

    class Meta:
        table_name = 'ip_location'


ip_location.create_table()
