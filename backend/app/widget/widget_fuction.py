import datetime
from ..model.widget_model import widget as widget_table
from ..base_model import Base
from ..login.login_funtion import User
from ..model.widget_model import widget_suite
from ..common_func import CommonFunc

cf = CommonFunc()


class Widget(Base):
    id = None
    name = None
    is_valid = None
    span = None
    buttons = None
    auto_update = None
    update_time = None

    def __init__(self, name=None, is_valid=None, span=None, buttons=None, auto_update=0, update_time=datetime.datetime.now(), id=0):
        self.name = name
        self.is_valid = is_valid
        self.span = span
        self.buttons = buttons
        self.auto_update = auto_update
        self.update_time = update_time
        self.id = id

    def complete(self):
        _ = widget_table.get(widget_table.id == self.id)
        self.name = _.name
        self.is_valid = _.is_valid
        self.span = _.span
        self.buttons = _.buttons
        self.auto_update = _.auto_update
        self.update_time = _.update_time
        return self


def widget_suite_get(user_id):
    _ = widget_suite.select().where(widget_suite.user_id == user_id).order_by(widget_suite.order).dicts()
    result = []
    for s_ in _:
        result.append({'id': s_['id'], 'name': s_['name'], 'name_ch': s_['name_ch'], 'order': s_['order'], 'detail': eval(s_['detail']), 'update_time': s_['update_time']})
    return result


def widget_get(user_id, suite_id):
    _ = widget_suite.get(widget_suite.id == suite_id)
    if int(_.user_id) != int(user_id):
        return []
    widget_id_list = eval(_.detail)
    return [cf.attr_to_dict(Widget(id=widget_id).complete()) for widget_id in widget_id_list]
