#! /usr/bin/env python3
import os
import sys
from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    try:
        port = int(sys.argv[1])
    except:
        print('未指定端口，使用默认端口50000')
        port = 50000
    config = {'host': '0.0.0.0', 'port': port, 'debug': True, 'ssl_context': ('homepage.crt', 'homepage.key')}
    try:
        app.run(**config)
    except:
        config.pop('ssl_context')
        app.run(**config)
