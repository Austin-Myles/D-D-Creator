from decouple import config

class Config(object):
    SECRET_KEY = config("SECRET_KEY", default="guess-me")
    SECURITY_PASSWORD_SALT = config("SECURITY_PASSWORD_SALT", default="very important")

    #Mail Settings
    MAIL_DEFAULT_SENDER = "noreply@flask.com"
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = False
    MAIL_USERNAME = config("MAIL_USERNAME")
    MAIL_PASSWORD = config("MAIL_PASSWORD")