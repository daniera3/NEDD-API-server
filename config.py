
class Config(object):
    DEBUG = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'neddproject@gmail.com'
    MAIL_PASSWORD = 'nedd123456'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True