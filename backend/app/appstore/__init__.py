from flask import Blueprint

appstore = Blueprint('appstore', __name__)
from . import api