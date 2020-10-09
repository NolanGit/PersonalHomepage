from peewee import DoesNotExist

from ..model.stock_model import stock as stock_table
from ..model.stock_model import stock_price, stock_belong


class Stock(object):
    id = 0
    code = None
    price_list = []

    def __init__(self, id=0, code=None):
        self.id = id
        if self.id != 0:
            self.code = stock_table.get_by_id(id).code
        else:
            self.code = code
            try:
                self.id = stock_table.get(stock_table.code == self.code).id
            except DoesNotExist:
                pass

    def _get_price(self, limit):
        stock_price_query = stock_price.select().where(stock_price.stock_id == self.id).dicts()
        self.price_list = [{
            'price': _['price'],
            'update_time': _['update_time'],
        } for _ in stock_price_query]
        return self
