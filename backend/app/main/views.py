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

@main.route('/favicon.ico', methods=['GET'])
@cross_origin()
def faviconico():
    with open("C:\\auto_test\\CrmTools\\vue\\dist\\favicon.ico", 'rb') as f:
        image = f.read()
    resp = Response(image, mimetype="image/jpeg")
    return resp