import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-wil-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    # MAIL_SERVER = os.environ.get('MAIL_SERVER') << this is what it SHOULD be
    MAIL_SERVER = 'localhost' # << this is what WORKS
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None << this is what it SHOULD be
    MAIL_USE_TLS = False # << this is what WORKS
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME') << this is what it SHOULD be
    MAIL_USERNAME = None # << this is what WORKS
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')<< this is what it SHOULD be
    MAIL_PASSWORD = None # << this is what WORKS
    ADMINS = ['phishadaptadmin@phishadapt.msc']