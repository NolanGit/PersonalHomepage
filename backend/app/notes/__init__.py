from flask import Blueprint

notes = Blueprint('notes', __name__)
from . import api