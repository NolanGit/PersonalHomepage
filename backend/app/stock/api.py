import time
import json
import requests
import datetime
import traceback
import collections
from flask_cors import cross_origin
from flask import render_template, session, redirect, url_for, current_app, flash, request, jsonify

from ..common_func import CommonFunc
from ..login.login_funtion import User
from ..response import Response as MyResponse
from ..privilege.privilege_control import privilegeFunction
from ..privilege.privilege_control import permission_required

from . import stock
from ..model.stock_model import stock as stock_table
from ..model.stock_model import stock_price, stock_belong

cf = CommonFunc()
rsp = MyResponse()

URL_PREFIX = '/stock'