class Config(object):
    DEBUG = False
    TESTING = False

    SECRET_KEY = '8027322a276aa2851f7191643805bc38b76a6a30e6db220af6d11068b768'

    MAIL_DEFAULT_SENDER = 'Jhaime Cando <no.reply.jhaime@gmail.com>'
    MAIL_USERNAME = 'no.reply.jhaime@gmail.com'
    MAIL_PASSWORD = 'nyxmzxfwtfgbpcvq'
    MAIL_PORT = 587
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_USE_TLS = True


class DevConfig(Config):
    DEBUG = True
    SECRET_KEY = 'dev'

    MAIL_DEBUG = True
