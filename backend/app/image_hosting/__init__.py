from flask import Blueprint

image_hosting = Blueprint('image_hosting', __name__)
from . import api
