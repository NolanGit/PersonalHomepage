import os
import peewee
from peewee import CharField, DateTimeField, IntegerField
from .model_function import BaseModel


class gold_price(BaseModel):
    price = CharField()
    update_time = DateTimeField()

    class Meta:
        table_name = 'gold_price'


class gold_price_push_option(BaseModel):
    user_id = IntegerField()
    is_valid = IntegerField()
    push_threshold = IntegerField()
    update_time = DateTimeField()

    class Meta:
        table_name = 'gold_price_push_option'


gold_price.create_table()
gold_price_push_option.create_table()