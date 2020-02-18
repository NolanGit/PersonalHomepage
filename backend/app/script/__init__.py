from flask import Blueprint

script = Blueprint('script', __name__)

from . import api
