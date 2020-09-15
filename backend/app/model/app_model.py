import os
import peewee
from peewee import CharField, IntegerField, DateTimeField
from .model_function import BaseModel


class app(BaseModel):
    name = CharField()
    url = CharField()
    user_id = IntegerField()
    expect_price = IntegerField()
    order = IntegerField()
    is_valid = IntegerField()
    update_time = DateTimeField()

    class Meta:
        table_name = 'app'


class app_price(BaseModel):
    app_id = IntegerField()
    price = CharField()
    update_time = DateTimeField()

    class Meta:
        table_name = 'app_price'


app.create_table()
app_price.create_table()