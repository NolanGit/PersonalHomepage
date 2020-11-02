from flask import Blueprint

news = Blueprint('news', __name__)

from . import api
