import os
import yaml
from app import app

basedir = os.path.abspath(os.path.dirname(__file__))


class dict2obj(object):
    def __init__(self, d):
        self.__dict__["d"] = d
        self.__dict__["d"]["env_type"] = env_type  # Hack to remember prod type

    def __getattr__(self, key):
        value = self.__dict__["d"][key]
        if type(value) == type({}):
            return dict2obj(value)
        return value


if os.environ.get("DEVELOPMENT"):
    app.logger.debug("Development config loaded")
    settings_file_name = "settings_DEV.yaml"
    env_type = "DEV"
else:
    app.logger.debug("Production config loaded")
    settings_file_name = "settings.yaml"
    env_type = "PROD"

with open(f"{basedir}/{settings_file_name}", "r") as settings_file:
    settings: dict = dict2obj(yaml.safe_load(settings_file))


class Configold(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "migrations/app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
