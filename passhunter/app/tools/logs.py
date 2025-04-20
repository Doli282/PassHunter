"""Error reporting"""
import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler

from flask import Flask

LOGGING_FORMAT = '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'

def set_mail_error_reporting(app: Flask) -> None:
    """
    Set mail error reporting base on environment variables

    Args:
        app (Flask): Flask application
    """
    if app.config['MAIL_SERVER']:
        auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']) if (app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']) else None
        secure = () if app.config['MAIL_USE_TLS'] else None
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='PassHunter Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


def set_rotating_log_file(app: Flask) -> None:
    """
    Set rotating log file base on environment variables

    Args:
        app (Flask): Flask application
    """
    # Create a log directory if it does not exist
    os.makedirs(app.config['LOGGING_DIR'], exist_ok=True)
    # Create a rotating log file handler
    file_handler = RotatingFileHandler(os.path.join(str(app.config['LOGGING_DIR']), str(app.config['LOGGING_FILE'])), maxBytes=10_000,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(LOGGING_FORMAT))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
