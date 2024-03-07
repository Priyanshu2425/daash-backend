from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SECRET_KEY'] = 'bestminorprojectever'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SESSION_COOKIE_SAMESITE'] = "None"

    db.init_app(app)
        
    from .views import views
    from .api import api
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(auth, url_prefix='/auth')

    from . import model
    with app.app_context():
        create_database()

    return app

def create_database():
    if not path.exists(f'instance/{DB_NAME}'):
        db.create_all()
        