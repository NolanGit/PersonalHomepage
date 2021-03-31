import os
import peewee
from peewee import CharField, IntegerField, DateTimeField, TextField
from .model_function import BaseModel


class news(BaseModel):
    website = TextField()
    category = TextField()
    content = TextField()
    create_time = DateTimeField()

    class Meta:
        table_name = 'news'


news.create_table()