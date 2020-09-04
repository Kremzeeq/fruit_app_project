
import os


class Config(object):
    #FLASK_APP = 'app.py'
    DEBUG = False
    TESTING = False
    SECRET_KEY = "B\xb2?.\xdf\x9f\xa7m\xf8\x8a%,\xf7\xc4\xfa\x91"

    FRUIT_CSV_PATH = "./static/assets/data_source/fruit.csv"
    DB_SERVER = 'localhost'
    DB_USERNAME = os.environ.get("FRUIT_APP_DB_USERNAME")
    DB_PASSWORD = os.environ.get("FRUIT_APP_DB_PASSWORD")
    UPDATE_FRUIT_AND_FACTS = True
    #FLASK_HOST = "0.0.0.0"
    HOST = "0.0.0.0"
    #FLASK_RUN_PORT = 8080
    RUN_PORT = 8080
    DB_NAME = 'celebration_of_fruit_production'

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'
    TESTING = True
    #FLASK_HOST = "localhost"
    HOST = "localhost"
    #FLASK_RUN_PORT = 5000
    RUN_PORT = 5000
    DB_NAME = 'celebration_of_fruit_development'
