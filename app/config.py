import os


class Configuration:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL") or "postgresql://insta_admin:passwordd@localhost/insta_app"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "0XO8Y7g|e^>H5{7yWE"
