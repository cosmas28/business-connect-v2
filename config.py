class Config(object):
    DEBUG = True
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']


class DevelopmentConfig(Config):
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
