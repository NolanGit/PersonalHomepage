from peewee import DoesNotExist

from ..base_model import Base

from ..model.fund_model import fund as fund_table
from ..model.fund_model import fund_price, fund_belong


class Fund(Base):
    id = 0
    code = None
    name = None
    price_list = []

    def __init__(self, code=None, name=None, id=0):
        self.id = id
        if self.id == 0:
            self.code = code
            self.name = name

    def get_price(self, limit):
        fund_price_query = fund_price.select().where(fund_price.fund_id == self.id).order_by(-fund_price.id).limit(150).dicts()
        self.price_list = [{'price': _['price'], 'range': _['range'], 'update_time': _['update_time'].strftime("%m-%d %H:%M")} for _ in fund_price_query[::-1]]
        return self

    def complete(self):
        self.base_complete(fund_table, ['price_list'])
        return self

    def save(self):
        self.base_save(fund_table, ['price_list'])
        return self

    def create(self):
        self.base_create(fund_table, ['price_list'])
        return self


class FundBelong(Base):
    id = 0
    fund_id = 0
    user_id = 0
    push = 0
    push_threshold = None
    is_valid = 0
    update_time = None

    def __init__(self, fund_id=0, user_id=0, push=0, push_threshold=None, is_valid=0, update_time=None, id=0):
        self.id = id
        if self.id == 0:
            self.fund_id = fund_id
            self.user_id = user_id
            self.push = push
            self.push_threshold = push_threshold
            self.is_valid = is_valid
            self.update_time = update_time

    def complete(self):
        self.base_complete(fund_belong)
        return self

    def save(self):
        self.base_save(fund_belong)
        return self

    def create(self):
        self.base_create(fund_belong)
        return self