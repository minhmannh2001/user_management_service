import logging
import logging.config
import os
from datetime import timedelta

import connexion

from app.databases.postgres import postgres_connection
from app.extensions.flask_migrate import migrate
from app.extensions.jwt_manager import jwt_manager
from app.models import User, user_roles, Role, UserProfile
from helpers.utils import load_config

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
APPLICATION_ROOT = os.path.join(MODULE_DIR, "..")


def create_app(config=None):
    app_config = config
    if app_config is None:
        config_file = os.path.join(APPLICATION_ROOT, "configs", "config.yaml")
        if os.path.isfile(config_file):
            app_config = load_config(config_file)
        else:
            raise Exception("No valid configuration was found")

    swagger_file = app_config.get("SWAGGER_FILE_PATH")
    if not swagger_file:
        raise Exception("SWAGGER_FILE_PATH is required in configuration file.")

    swagger_dir, swagger_filename = os.path.split(swagger_file)

    app = connexion.App(__name__, specification_dir=swagger_dir)

    flask_app = app.app
    flask_app.instance_path = MODULE_DIR
    flask_app.config.from_mapping(app_config)

    public_key = app_config.get("PUBLIC_KEY")

    flask_app.config["JWT_PUBLIC_KEY"] = public_key
    flask_app.config["JWT_ALGORITHM"] = "RS256"
    flask_app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    flask_app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

    app.add_api(swagger_filename)

    configure_app(flask_app)

    return flask_app


def configure_app(app):
    configure_log_handlers(app)
    configure_databases(app)
    configure_extensions(app)


def configure_log_handlers(app):
    logging_config_file = os.path.join(APPLICATION_ROOT, app.config["LOGGER_CONFIG_PATH"])
    logging.config.fileConfig(logging_config_file)
    logger = logging.getLogger("root")

    for handler in logger.root.handlers:
        app.logger.addHandler(handler)
        app.logger.propagate = False

    app.logger.error("Start logging API services at the error level.")
    app.logger.debug("Start logging API services at the debug level.")


def configure_databases(app):
    configure_postgres_connection(app)


def configure_postgres_connection(app):
    postgres_connection.init_app(app)
    with app.app_context():
        postgres_connection.db.create_all()


def configure_extensions(app):
    jwt_manager.init_app(app)
    migrate.init_app(app, postgres_connection.db)
