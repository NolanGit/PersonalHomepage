from peewee import DoesNotExist

from ..base_model import Base

from ..model.stock_model import stock as stock_table
from ..model.stock_model import stock_price, stock_belong


class Stock(Base):
    id = 0
    code = None
    name = None
    market = None
    price_list = []

    def __init__(self, code=None, name=None, market=None, id=0):
        self.id = id
        if self.id == 0:
            self.code = code
            self.name = name
            self.market = market

    def get_price(self, limit):
        stock_price_query = stock_price.select().where(stock_price.stock_id == self.id).order_by(-stock_price.id).limit(150).dicts()
        self.price_list = [{'price': _['price'], 'range': _['range'], 'update_time': _['update_time'].strftime("%m-%d %H:%M")} for _ in stock_price_query[::-1]]
        return self

    def complete(self):
        self.base_complete(stock_table, ['price_list'])
        return self

    def save(self):
        self.base_save(stock_table, ['price_list'])
        return self

    def create(self):
        self.base_create(stock_table, ['price_list'])
        return self


class StockBelong(Base):
    id = 0
    stock_id = 0
    user_id = 0
    push = 0
    push_threshold = None
    is_valid = 0
    update_time = None

    def __init__(self, stock_id=0, user_id=0, push=0, push_threshold=None, is_valid=0, update_time=None, id=0):
        self.id = id
        if self.id == 0:
            self.stock_id = stock_id
            self.user_id = user_id
            self.push = push
            self.push_threshold = push_threshold
            self.is_valid = is_valid
            self.update_time = update_time

    def complete(self):
        self.base_complete(stock_belong)
        return self

    def save(self):
        self.base_save(stock_belong)
        return self

    def create(self):
        self.base_create(stock_belong)
        return self