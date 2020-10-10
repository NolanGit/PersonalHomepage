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

    def base_complete(self, table):
        self_dict = cf.attr_to_dict(self)
        if 'id' in self_dict:
            _ = table.get(table.id == self_dict['id'])
            for key in self_dict:
                self_dict[key] = _[key]
        else:
            raise AttributeError
        return self

    def base_create(self, table, pop_attr=[]):
        self_dict = cf.attr_to_dict(self)
        if 'id' in self_dict:
            self_dict.pop('id')
        for attr in pop_attr:
            self_dict.pop(attr)
        _ = table.create(**self_dict)
        self.id = _.id
        return self

    def base_save(self, table, pop_attr=[]):
        self_dict = cf.attr_to_dict(self)
        _id = self_dict.pop('id')
        for attr in pop_attr:
            self_dict.pop(attr)
        if 'create_time' in self_dict:
            self_dict['create_time'] = datetime.datetime.now()
        table.update(**self_dict).where(table.id == _id).execute()
        return self
