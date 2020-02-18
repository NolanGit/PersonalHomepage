from flask import Blueprint

weather = Blueprint('weather', __name__)
from . import api