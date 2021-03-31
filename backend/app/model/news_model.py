import os
import peewee
from peewee import CharField, IntegerField, DateTimeField
from .model_function import BaseModel


class news(BaseModel):
    news_json = CharField()
    create_time = DateTimeField()

    class Meta:
        table_name = 'news'

news.create_table()