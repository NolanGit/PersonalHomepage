from flask import Blueprint

widget = Blueprint('widget', __name__)
from . import api