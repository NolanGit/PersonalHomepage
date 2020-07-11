from flask import Blueprint

cloud_drive = Blueprint('cloud_drive', __name__)
from . import api