from flask import Blueprint

console = Blueprint('console', __name__)
from . import api