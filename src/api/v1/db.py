from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
jwt = JWTManager()
api =  Api()
bcrypt = Bcrypt()
mail = Mail()


def setup_with_app(main_app):
    db.init_app(main_app)
    migrate.init_app(main_app, db)
    ma.init_app(main_app)
    jwt.init_app(main_app)
    api.init_app(main_app)
    bcrypt.init_app(main_app)
    mail.init_app(main_app)
