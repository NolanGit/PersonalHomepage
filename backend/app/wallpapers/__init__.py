from flask import Blueprint

wallpapers = Blueprint('wallpapers', __name__)
from . import api