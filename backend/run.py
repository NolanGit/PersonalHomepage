#! /usr/bin/env python3
import os
import sys
import configparser
from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

cf = configparser.ConfigParser()
cf.read('app/homepage.config')
try:
    HTTPS = cf.get('config', 'HTTPS')
except:
    HTTPS = False

if __name__ == '__main__':
    try:
        port = int(sys.argv[1])
    except:
        print('未指定端口，使用默认端口50000')
        port = 50000
    if HTTPS:
        app.run(host = '0.0.0.0', port = port, debug = True, ssl_context = ('homepage.crt', 'homepage.key'))
    else:
        app.run(host = '0.0.0.0', port = port, debug = True)
