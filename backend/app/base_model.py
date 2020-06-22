import time
import json
import datetime
from functools import wraps
try:
    from .common_func import CommonFunc
except:
    from common_func import CommonFunc

cf = CommonFunc()

class Base(object):
    def base_create(self, table):
        aaa = cf.attr_to_dict(self)
        aaa.pop('id')
        _ = table.create(**aaa)
        self.id = _.id
        return self

    def base_save(self, table):
        aaa = cf.attr_to_dict(self)
        _id = aaa.pop('id')
        aaa['create_time'] = datetime.datetime.now()
        table.update(**aaa).where(table.id == _id).execute()
        return self
