import os


class Config(object):
    FLASK_ENV = os.getenv("FLASK_ENV")
    FLASK_DEBUG = os.getenv("FLASK_DEBUG")
    FLASK_HOST = os.getenv("FLASK_HOST")
    FLASK_PORT = os.getenv("FLASK_PORT")
    API_BASE_URL = os.getenv("API_BASE_URL")
    FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
    SQLALCHEMY_SCHEMA = os.getenv("SQLALCHEMY_SCHEMA")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False
