import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# TOP_LEVEL_DIR = os.path.abspath(os.curdir)
class Config(object):
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY', "the-secret-is-safe")
    MYSQL_DATABASE_HOST = os.environ.get('MYSQL_DATABASE_HOST', '127.0.0.1')
    MYSQL_DATABASE_PORT = os.environ.get("MYSQL_DATABASE_PORT", 3306)
    MYSQL_DATABASE_USER = os.environ.get('MYSQL_DATABASE_USER', 'root')
    MYSQL_DATABASE_PASSWORD = os.environ.get('MYSQL_DATABASE_PASSWORD')
    MYSQL_MASTER_SCHEMA = os.environ.get('MYSQL_MASTER_SCHEMA', 'dev')
    MYSQL_DATABASE_CHARSET = os.environ.get("MYSQL_DATABASE_CHARSET", "utf-8")

class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    TESTING = True

class StagingConfig(Config):
    DEBUG = False
    LOG_LEVEL = 'INFO'

class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = 'WARNING'

config_by_name = {
    'development': DevelopmentConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
