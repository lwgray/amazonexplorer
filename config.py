"""Config Setting for Flask App"""
import os
print "Running Nedcow-Dev Server"


class Config(object):
    """Global Settings"""
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    POSTMARK_API_KEY = os.environ['POSTMARK_API_KEY']
    POSTMARK_SENDER = 'lwgray@gmail.com'
    UPLOAD_FOLDER = 'documents'
    MWS_SIMPLE = os.environ['MWS_SIMPLE']
    MWS_SHACK = os.environ['MWS_SHACK']
    AWS_ID = os.environ['AWS_ID']
    AWS_KEY = os.environ['AWS_KEY']


class DevelopmentConfig(Config):
    """ Development Settings """
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    """ Testing Settings """
    TESTING = True
