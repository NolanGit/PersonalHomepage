import os
import peewee
from peewee import CharField, IntegerField, DateTimeField, FloatField
from .model_function import BaseModel


class fund(BaseModel):
    code = CharField()
    name = CharField()

    class Meta:
        table_name = 'fund'


class fund_price(BaseModel):
    fund_id = IntegerField()
    price = FloatField()
    range = FloatField()
    update_time = DateTimeField()

    class Meta:
        table_name = 'fund_price'


class fund_belong(BaseModel):
    fund_id = IntegerField()
    user_id = IntegerField()
    push = IntegerField()
    push_threshold = CharField()
    is_valid = IntegerField()
    update_time = DateTimeField()

    class Meta:
        table_name = 'fund_belong'


fund.create_table()
fund_price.create_table()
fund_belong.create_table()