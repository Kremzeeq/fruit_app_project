
import os


class Config(object):
    FLASK_APP = 'fruit_app'
    DEBUG = False
    TESTING = False
    SECRET_KEY = "B\xb2?.\xdf\x9f\xa7m\xf8\x8a%,\xf7\xc4\xfa\x91"
    #FLASK_RUN_PORT = 5001
    FRUIT_CSV_PATH = "./static/assets/data_source/fruit.csv"
    DB_SERVER = None
    DB_NAME = None
    DB_USERNAME = os.environ.get("FRUIT_APP_DB_USERNAME")
    DB_PASSWORD = os.environ.get("FRUIT_APP_DB_PASSWORD")
    UPDATE_FRUIT_AND_FACTS = True


class ProductionConfig(Config):
    """
    DB_SERVER should be provided in format e.g. '192.168.19.32'
    This should be the IPv4 Public IP.
    """
    DB_SERVER = os.environ.get("PRODUCTION_DB_SERVER")
    DB_NAME = 'celebration_of_fruit_production'


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'
    TESTING = True
    DB_SERVER = 'localhost'
    DB_NAME = 'celebration_of_fruit_development'