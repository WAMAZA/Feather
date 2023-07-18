import binascii
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
    BASE_FOLDER = os.getcwd()
    UPLOAD_FOLDER = os.path.join(os.getcwd(),"uploaded_files/product")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 Megabyte
    SECRET_KEY = binascii.hexlify(os.urandom(24))
    DEBUG = True
    ENV = "development"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'users.db')

class ProductionConfig(BaseConfig):
    pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True
