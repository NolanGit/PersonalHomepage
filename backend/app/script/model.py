import datetime
from ..base_model import Base
from ..model.script_model import script_sub_system


class ScriptSubSystem(Base):
    id = 0
    name = None
    user_id = None
    is_valid = None
    update_time = None

    def __init__(self, id=0, name=None, user_id=None, is_valid=1, update_time=datetime.datetime.now()):
        self.id = id
        self.name = name
        self.user_id = user_id
        self.is_valid = is_valid
        self.update_time = update_time

    def create(self):
        self.base_create(script_sub_system)

    def delete(self):
        pass