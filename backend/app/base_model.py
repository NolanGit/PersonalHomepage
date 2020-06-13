import time
import json
import datetime
from functools import wraps
from .common_func import CommonFunc

cf = CommonFunc()

class Base(object):
    def create(self, table):
        aaa = cf.attr_to_dict(self)
        aaa.pop('id')
        _ = table.create(**aaa)
        self.id = _.id
        return self

    def save(self, table):
        aaa = cf.attr_to_dict(self)
        _id = aaa.pop('id')
        aaa['create_time'] = datetime.datetime.now()
        table.update(**aaa).where(table.id == _id).execute()
        return self
