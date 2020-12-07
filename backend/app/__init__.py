import os
import sys
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
sys.path.append(currentUrl)
from flask import Flask
from flask_cors import CORS
from .model.model_function import BaseDb
from playhouse.flask_utils import FlaskDB


def create_app(config_name):
    app = Flask(__name__, static_folder="../../dist/static", template_folder="../../dist")
    FlaskDB(app, BaseDb().db)  # 解决peewee不自动关闭连接池连接，参见https://www.cnblogs.com/xueweihan/p/6698456.html
    CORS(app, supports_credentials=True)

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

    from .notes import notes as notes_blueprint
    app.register_blueprint(notes_blueprint, url_prefix='/notes')

    from .short_url import short_url as short_url_blueprint
    app.register_blueprint(short_url_blueprint, url_prefix='/s')

    from .image_hosting import image_hosting as image_hosting_blueprint
    app.register_blueprint(image_hosting_blueprint, url_prefix='/imageHosting')

    from .translator import translator as translator_blueprint
    app.register_blueprint(translator_blueprint, url_prefix='/translator')

    from .wallpapers import wallpapers as wallpapers_blueprint
    app.register_blueprint(wallpapers_blueprint, url_prefix='/wallpapers')

    from .stock import stock as stock_blueprint
    app.register_blueprint(stock_blueprint, url_prefix='/stock')

    from .fund import fund as fund_blueprint
    app.register_blueprint(fund_blueprint, url_prefix='/fund')

    from .news import news as news_blueprint
    app.register_blueprint(news_blueprint, url_prefix='/news')

    return app
