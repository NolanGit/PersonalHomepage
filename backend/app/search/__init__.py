from flask import Blueprint

search = Blueprint('search', __name__)
from . import api