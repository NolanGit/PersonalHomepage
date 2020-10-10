import datetime
import traceback
from ..base_model import Base
from peewee import DoesNotExist
from ..model.notes_model import notes as notes_table


class Notes(Base):
    id = None
    name = None
    content = None
    user_id = None
    is_valid = None
    update_time = None

    def __init__(self, id=0, name=None, content=None, user_id=None, is_valid=None, update_time=datetime.datetime.now()):
        self.id = id
        self.name = name
        self.content = content
        self.user_id = user_id
        self.is_valid = is_valid
        self.update_time = update_time

    def save(self):
        self.base_save(notes_table)

    def create(self):
        self.base_create(notes_table)
