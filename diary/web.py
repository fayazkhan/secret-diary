from flask import Flask
from flask_admin import Admin


def application_factory():
    application = Flask(__name__)
    Admin(application)
    return application
