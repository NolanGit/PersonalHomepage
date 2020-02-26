from flask import Blueprint

try:
    login = Blueprint('login', __name__)
    from . import api
except:
    pass