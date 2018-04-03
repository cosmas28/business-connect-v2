class Config(object):
    DEBUG = True
    SECRET_KEY = '21%hbba7&njb#ggj@'
    JWT_SECRET_KEY = 'jwt_secret_string'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']


class DevelopmentConfig(Config):
    SQLALCHEMY_ECHO = True
    SWAGGER = {'title': 'WeConnect v2.0', 'uiversion': 2}


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
