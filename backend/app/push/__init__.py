from flask import Blueprint

if __name__=='app.push':
    push = Blueprint('push', __name__)
    from . import api