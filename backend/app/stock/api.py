import time
import json
import requests
import datetime
import traceback
import urllib.request
from . import stock
from flask_cors import cross_origin
from flask import render_template, session, redirect, url_for, current_app, flash, Response, request, jsonify
from .model import stock, stock_detail
from ..common_func import User
