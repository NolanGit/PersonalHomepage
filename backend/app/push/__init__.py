from flask import Blueprint

push = Blueprint('push', __name__)
from . import api