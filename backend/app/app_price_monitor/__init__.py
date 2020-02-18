from flask import Blueprint

app_price_monitor = Blueprint('app_price_monitor', __name__)
from . import api