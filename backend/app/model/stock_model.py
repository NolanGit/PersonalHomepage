import os
import peewee
from peewee import CharField, IntegerField, DateTimeField, FloatField
from .model_function import BaseModel


class stock(BaseModel):
    code = CharField()
    name = CharField()
    market = IntegerField()  # 1:SH; 2:SZ; 3:HK; 4:US;

    class Meta:
        table_name = 'stock'


class stock_price(BaseModel):
    stock_id = IntegerField()
    price = FloatField()
    range = FloatField()
    update_time = DateTimeField()

    class Meta:
        table_name = 'stock_price'


class stock_belong(BaseModel):
    stock_id = IntegerField()
    user_id = IntegerField()
    push = IntegerField()
    push_threshold = CharField()
    is_valid = IntegerField()
    update_time = DateTimeField()

    class Meta:
        table_name = 'stock_belong'


stock.create_table()
stock_price.create_table()
stock_belong.create_table()