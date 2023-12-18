import os

project_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ['SECRET_KEY']


class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    pass


config_dict = {'develop': DevelopmentConfig,
               'product': ProductionConfig}