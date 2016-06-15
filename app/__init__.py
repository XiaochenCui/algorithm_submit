import os

from flask import Flask, request, session
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.pagedown import PageDown

from flask_babelex import Babel

from config import config
from flask_admin import Admin

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

# 创建files文件夹
file_path = os.path.join(os.path.dirname(__file__), 'static/data')
try:
    os.mkdir(file_path)
except OSError:
    pass


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    from app.admin.views import admin
    admin.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # 初始化 babel
    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        override = request.args.get('lang')

        if override:
            session['lang'] = override

        return session.get('lang', 'zh_CN')

    return app
