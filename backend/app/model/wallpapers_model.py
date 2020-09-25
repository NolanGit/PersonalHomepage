import os
import peewee
from peewee import CharField, IntegerField, DateTimeField, DateField
from .model_function import BaseModel


class wallpapers(BaseModel):
    date = CharField()
    url = CharField()
    size = CharField()
    copyright = CharField()
    copyrightlink = CharField()
    update_time = DateTimeField()

    class Meta:
        table_name = 'wallpapers'


wallpapers.create_table()