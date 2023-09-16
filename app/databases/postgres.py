from flask_sqlalchemy import SQLAlchemy


class PostgresConnection:
    def __init__(self):
        self.db = SQLAlchemy()

    def init_app(self, app):
        self.db.init_app(app)


postgres_connection = PostgresConnection()
