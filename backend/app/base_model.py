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
        self_dict = cf.attr_to_dict(self)
        if 'id' in self_dict:
            self_dict.pop('id')
        _ = table.create(**self_dict)
        self.id = _.id
        return self

    def base_save(self, table):
        self_dict = cf.attr_to_dict(self)
        _id = self_dict.pop('id')
        self_dict['create_time'] = datetime.datetime.now()
        table.update(**self_dict).where(table.id == _id).execute()
        return self
