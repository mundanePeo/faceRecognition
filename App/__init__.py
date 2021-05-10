from flask import Flask
from config.configLoad import config_data
from App.exts import init_ext
from App.views import init_api
# from App.views import init_blueprint
from App.settings import envs


import time
import os


def create_app():
    app = Flask(__name__, template_folder=settings.TEMPLATE_FOLDER)
    # 配置加载
    app.config.from_object(envs.get(config_data['mode']))
    # 初始化蓝图
    # init_blueprint(app)
    # 初始化api
    init_api(app)
    # 初始化各种第三方库
    init_ext(app)
    return app
