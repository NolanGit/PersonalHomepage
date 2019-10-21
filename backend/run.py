#! /usr/bin/env python3
import os
from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
