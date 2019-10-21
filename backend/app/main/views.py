import re
import time
import requests
import datetime

from flask import render_template, session, redirect, url_for, current_app, request,jsonify
from . import main
from flask_cors import cross_origin

@main.route('/', defaults={'path': ''})
@main.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")