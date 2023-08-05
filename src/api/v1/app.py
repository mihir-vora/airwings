from flask import Flask
from db import setup_with_app
from apps.auth.urls import auth_bp
from apps.flights.urls import flight_bp
from apps.flight_search.urls import flight_search
# from apps.booking.urls import booking_bp

from apps.auth.models import *
from apps.flights.models import *
# from apps.booking.models import *

def register_blueprint(main_app):
    main_app.register_blueprint(auth_bp)
    main_app.register_blueprint(flight_bp)
    # main_app.register_blueprint(booking_bp)
    main_app.register_blueprint(flight_search)
    
def email_config(main_app):
    main_app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Replace with your email provider's SMTP server
    main_app.config['MAIL_PORT'] = 587
    main_app.config['MAIL_USE_TLS'] = True
    main_app.config['MAIL_USERNAME'] = 'er.voramihir@gmail.com'  # Replace with your email address
    main_app.config['MAIL_PASSWORD'] = 'gqypjgoxesojgfoc'  # Replace with your email password

def create_app():
    main_app = Flask(__name__, instance_relative_config=True)
    main_app.config.from_pyfile('.env')
    main_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    main_app.config['SECRET_KEY'] =  'kjfjk1kj2kjkj32jkjksj2j1kjk1jwewkjfjsfkjbk2jkjkj'
    main_app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 86400
    email_config(main_app)
    register_blueprint(main_app)
    setup_with_app(main_app)
    return main_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)