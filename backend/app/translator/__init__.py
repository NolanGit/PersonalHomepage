from flask import Blueprint

translator = Blueprint('translator', __name__)
from . import api
