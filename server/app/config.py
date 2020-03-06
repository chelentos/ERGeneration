from datetime import timedelta

class Config:

    DEBUG = True

    # Flask
    SECRET_KEY = "secret key"

    # Flask-session
    PERMANENT_SESSION_LIFETIME = timedelta(days=365)

    # Flask-login
    REMEMBER_COOKIE_DURATION = timedelta(days=365)

    # MONGODB
    MONGODB_SETTINGS = {
      'db': 'ergeneration',
      'host': 'mongodb://er-ad:t100km0201@localhost:27017/er-gen?authSource=er-gen'
    }

    # WTForms
    WTF_CSRF_CHECK_DEFAULT = False