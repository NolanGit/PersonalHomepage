from flask import Blueprint

short_url = Blueprint('short_url', __name__)
from . import api