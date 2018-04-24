# config.py
"""Define configuration for different development stages."""

import os


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    JWT_SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    SWAGGER = {'title': 'WeConnect v2.0', 'uiversion': 2}


class DevelopmentConfig(Config):
    """Configuration for Development."""
    DEBUG = True
    CSRF_ENABLED = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL_DEV')


class TestingConfig(Config):
    """Configuration for testing stage."""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = \
        "postgresql://test_user:default@localhost/test_db"


class StagingConfig(Config):
    """Configurations for Staging."""

    DEBUG = True


class ProductionConfig(Config):
    """Configuration for production stage."""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig
}
