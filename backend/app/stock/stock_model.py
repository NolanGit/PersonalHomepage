from model.stock_model import stock as stock_table
from model.stock_model import stock_price, stock_belong


class Stock(object):
    id = None
    price_list = []

    def __init__(self, id):
        self.id = id

    def _get_price(self, limit):
        stock_price_query = stock_price.select().where(stock_price.stock_id == self.id).dicts()
        self.price_list = [{
            'price': _['price'],
            'update_time': _['update_time'],
        } for _ in stock_price_query]
        return self

    