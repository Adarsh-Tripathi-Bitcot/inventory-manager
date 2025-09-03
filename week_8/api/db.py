"""Database and migration initialization module."""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#: SQLAlchemy instance for database access
db: SQLAlchemy = SQLAlchemy()

#: Flask-Migrate instance for handling migrations
migrate: Migrate = Migrate()
