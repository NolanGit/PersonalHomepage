import os
import peewee
from peewee import CharField, IntegerField, DateTimeField
from .model_function import BaseModel


class console(BaseModel):
    name = CharField()
    order = IntegerField()
    icon = CharField(null=True)
    component_name = CharField(null=True)
    is_valid = IntegerField(null=True)
    update_time = DateTimeField(null=True)

    class Meta:
        table_name = 'console'

class icon(BaseModel):
    name = CharField()

    class Meta:
        table_name = 'icon'

console().create_table()
icon().create_table()