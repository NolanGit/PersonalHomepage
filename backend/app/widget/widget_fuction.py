import datetime
from ..model.widget_model import widget as widget_table
from ..base_model import Base
from ..login.login_funtion import User


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
        _ = widget_table.get(widget_table.id == id)
        self.name = _.name
        self.is_valid = _.is_valid
        self.span = _.span
        self.buttons = _.buttons
        self.auto_update = _.auto_update
        self.update_time = _.update_time
        return self
