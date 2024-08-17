from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager 
# __init__ created to allow website to become a package to be imported

db = SQLAlchemy()
DB_NAME = "database.db" # Creating SQL database

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'kadens secretcode'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # Assigning database to website folder
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/') # Register blueprints
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    login_manager = LoginManager() # Initialize Login Manager 
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) # Flask - find this user by ID

    with app.app_context():
        db.create_all()

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME): # Creates database if there is not one already
        db.create_all(app=app)
        print('Created Database!')
