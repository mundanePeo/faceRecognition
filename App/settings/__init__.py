from config.configLoad import config_data

import os

# os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 与 os.path.dirname(os.path.dirname(__file__))
# 相同，都返回/home/user/mld/faceRecognize/App

BASE_DIR = os.getcwd()  # 返回/home/user/mld/faceRecognize
TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'templates')

# logger
MESSAGE_DATA_FORMAT = "%Y-%m-%d %H:%M:%S"
DIR_DATA_FORMATE = "%Y%m%d_%H%M%S"
DIR_OUTPUT = os.path.join(BASE_DIR, 'doc/log')

# info saved in mysql
INFO = ["area", "cam", "face_id", "face_feature"]
DIR_FEATURE_SAVE = os.path.join(BASE_DIR, 'doc/faces_feature')
FILE_FACE_IDS = os.path.join(BASE_DIR, 'doc/face_ids.txt')


def get_db_uri(dbinfo):
    # 获取值，如果不存在则给出默认值
    BACKEND = dbinfo.get('BACKEND') or 'mysql'
    DRIVER = dbinfo.get('DRIVER') or 'pymysql'
    USER = dbinfo.get('USER') or 'root'
    PASSWORD = dbinfo.get('PASSWORD') or '123456',
    HOST = dbinfo.get('HOST') or '192.168.0.90'  # 'localhost'
    PORT = dbinfo.get('PORT') or '3306'
    DB = dbinfo.get('DB') or 'face_db'
    return "{}+{}://{}:{}@{}:{}/{}".format(BACKEND, DRIVER, USER, PASSWORD, HOST, PORT, DB)


class Config:
    SECRET_KEY = 'WEBACE'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# 不同的环境有不同的配置
class DevelopConfig(Config):
    DEBUG = True

    DATABASE = {
        'BACKEND': 'mysql',
        'DRIVER': 'pymysql',
        'USER': config_data['mysql_dev']['user'],
        'PASSWORD': config_data['mysql_dev']['password'],
        'HOST': config_data['mysql_dev']['host'],
        'PORT': config_data['mysql_dev']['port'],
        'DB': config_data['mysql_dev']['db']
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(DATABASE)


class TestingConfig(Config):
    TESTING = True

    DATABASE = {
        'BACKEND': 'mysql',
        'DRIVER': 'pymysql',
        'USER': config_data['mysql_test']['user'],
        'PASSWORD': config_data['mysql_test']['password'],
        'HOST': config_data['mysql_test']['host'],
        'PORT': config_data['mysql_test']['port'],
        'DB': config_data['mysql_test']['db']
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(DATABASE)


# 演示环境
class StagingConfig(Config):
    DATABASE = {
        'BACKEND': 'mysql',
        'DRIVER': 'pymysql',
        'USER': config_data['mysql_staging']['user'],
        'PASSWORD': config_data['mysql_staging']['password'],
        'HOST': config_data['mysql_staging']['host'],
        'PORT': config_data['mysql_staging']['port'],
        'DB': config_data['mysql_staging']['db']
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(DATABASE)


# 生产环境
class ProductConfig(Config):
    DATABASE = {
        'BACKEND': 'mysql',
        'DRIVER': 'pymysql',
        'USER': config_data['mysql_product']['user'],
        'PASSWORD': config_data['mysql_product']['password'],
        'HOST': config_data['mysql_product']['host'],
        'PORT': config_data['mysql_product']['port'],
        'DB': config_data['mysql_product']['db']
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(DATABASE)


envs = {
    "develop": DevelopConfig,
    "Testing": TestingConfig,
    "staging": StagingConfig,
    "product": ProductConfig,
}
