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

class news_new(BaseModel):
    website = TextField()
    category = TextField()
    name = TextField()
    url = TextField()
    create_time = DateTimeField()


news.create_table()
news_new.create_table()