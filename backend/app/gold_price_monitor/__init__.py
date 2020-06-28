from flask import Blueprint

app_price_monitor = Blueprint('gold_price_monitor', __name__)
from . import api