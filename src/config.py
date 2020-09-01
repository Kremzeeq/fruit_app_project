


class Config(object):
    FLASK_APP = 'fruit_app'
    DEBUG = False
    TESTING = False
    SECRET_KEY = "B\xb2?.\xdf\x9f\xa7m\xf8\x8a%,\xf7\xc4\xfa\x91"
    FLASK_RUN_PORT = 5001



class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'
    TESTING = True