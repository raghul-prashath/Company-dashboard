from datetime import timedelta 
import os

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'secret_key'
    JWT_SECRET_KEY = 'secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///coredata.db'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(
    #     os.getenv('R3s3Olw2kc'),
    #     os.getenv('YHEz5dqU4P'),
    #     os.getenv('remotemysql.com'),
    #     os.getenv('R3s3Olw2kc')
    #     )

    #User, Pass, host, db name
    SQLALCHEMY_TRACK_MODIFICATIONS= True
    COOKIE_SECURE = False
    ACCESS_COOKIE_NAME = 'access_token_cookie'
    REFRESH_COOKIE_NAME = 'refresh_token_cookie'
    JWT_TOKEN_LOCATION = 'cookies'
    JWT_SESSION_COOKIE = True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=3)
    JWT_COOKIE_CSRF_PROTECT = False
        
class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
