
import os


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "B\xb2?.\xdf\x9f\xa7m\xf8\x8a%,\xf7\xc4\xfa\x91"
    FRUIT_CSV_PATH = "./static/assets/data_source/fruit.csv"
    DB_SERVER = 'localhost'
    DB_USERNAME = os.environ.get("DB_USERNAME")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    UPDATE_FRUIT_AND_FACTS = os.environ.get("UPDATE_FRUIT_AND_FACTS")
    HOST = "0.0.0.0"
    RUN_PORT = 8080
    DB_NAME = 'celebration_of_fruit_production'

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    HOST = "localhost"
    RUN_PORT = 5000
    DB_NAME = 'celebration_of_fruit_development'
