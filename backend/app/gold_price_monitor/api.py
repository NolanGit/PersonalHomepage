import time
import json
import requests
import datetime
import traceback
import urllib.request
from . import app_price_monitor
from flask_cors import cross_origin
from flask import session, redirect, url_for, current_app, flash, Response, request, jsonify
from ..model.gold_price_model import gold_price as gold_price_table
from ..login.login_funtion import User
from ..privilege.privilege_control import permission_required
from .gold_price_function import *

URL_PREFIX = '/gold'