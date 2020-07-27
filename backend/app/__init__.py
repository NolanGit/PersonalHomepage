import os
import sys
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
sys.path.append(currentUrl)
from flask import Flask
from config import config
from flask_cors import CORS
from .model.model_function import db
from playhouse.flask_utils import FlaskDB


def create_app(config_name):
    app = Flask(__name__, static_folder="../../dist/static", template_folder="../../dist")
    FlaskDB(app, db)  # 解决peewee不自动关闭连接池连接，参见https://www.cnblogs.com/xueweihan/p/6698456.html
    CORS(app, supports_credentials=True)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .widget import widget as widget_blueprint
    app.register_blueprint(widget_blueprint, url_prefix='/widget')

    from .cloud_drive import cloud_drive as cloud_drive_blueprint
    app.register_blueprint(cloud_drive_blueprint, url_prefix='/cloudDrive')

    from .search import search as search_blueprint
    app.register_blueprint(search_blueprint, url_prefix='/search')

    from .login import login as login_blueprint
    app.register_blueprint(login_blueprint, url_prefix='/login')

    from .weather import weather as weather_blueprint
    app.register_blueprint(weather_blueprint, url_prefix='/weather')

    from .bookmarks import bookmarks as bookmarks_blueprint
    app.register_blueprint(bookmarks_blueprint, url_prefix='/bookmarks')

    from .console import console as console_blueprint
    app.register_blueprint(console_blueprint, url_prefix='/console')

    from .script import script as script_blueprint
    app.register_blueprint(script_blueprint, url_prefix='/script')

    from .privilege import privilege as privilege_blueprint
    app.register_blueprint(privilege_blueprint, url_prefix='/privilege')

    from .app_price_monitor import app_price_monitor as app_price_monitor_blueprint
    app.register_blueprint(app_price_monitor_blueprint, url_prefix='/app')

    from .push import push as push_blueprint
    app.register_blueprint(push_blueprint, url_prefix='/push')

    from .gold_price_monitor import gold_price_monitor as gold_price_monitor_blueprint
    app.register_blueprint(gold_price_monitor_blueprint, url_prefix='/gold')

    from .notes_price_monitor import notes_price_monitor as notes_price_monitor_blueprint
    app.register_blueprint(notes_price_monitor_blueprint, url_prefix='/notes')

    return app
