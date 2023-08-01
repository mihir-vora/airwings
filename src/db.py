from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()

def setup_with_app(main_app):
    db.init_app(main_app)
    migrate.init_app(main_app, db)

