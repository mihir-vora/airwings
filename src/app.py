from flask import Flask
from db import setup_with_app

def register_blueprint(main_app):
    pass
def create_app():
    main_app = Flask(__name__, instance_relative_config=True)
    main_app.config.from_pyfile('.env')
    main_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    main_app.config['SECRET_KEY'] =  'kjfjk1kj2kjkj32jkjksj2j1kjk1jwewkjfjsfkjbk2jkjkj'
    register_blueprint(main_app)
    setup_with_app(main_app)
    return main_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)