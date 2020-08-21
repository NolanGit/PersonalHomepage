from flask import Blueprint

image_cloud = Blueprint('image_cloud', __name__)
from . import api
