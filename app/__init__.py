# Import libraries
from flask import Flask
import os # For use with logging
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask_mail import Mail

# Instantiate DB class and migration config
db = SQLAlchemy()
migrate = Migrate()

# Instantiate login class and set class methods
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'

# Instantiate mail class
mail = Mail()

# Main web application function
def create_app(config_class=Config):
    # Instantiate web application class instance
    app = Flask(__name__)
    # Set configuration options for class
    app.config.from_object(config_class)

    # Initialise classes
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)

    # Register blueprints with web application
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.training import bp as training_bp
    app.register_blueprint(training_bp, url_prefix='/training')
    
    # Set error logging to email administrators when web app not in debug mode
    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='PhishAdapt Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        # Create logs folder if it doesn't already exist
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/phishadapt.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        # Set logger default logging level to INFO
        app.logger.setLevel(logging.INFO)

        # Set default text for logger log entries
        app.logger.info('PhishAdapt startup')

    return app