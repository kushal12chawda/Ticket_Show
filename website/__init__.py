from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy 
from os import path
from flask_login import LoginManager

db = SQLAlchemy()

def create():
    app=Flask(__name__)
    app.config['SECRET_KEY'] = 'kushalisasecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db" 
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User,Admin

    create_database(app)

    login_manager = LoginManager()
    login_manager.blueprint_login_views = {
        'user': 'auth.login_post_user',
        'admin': 'auth.login_post_admin',
    }
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(id):
        x = User.query.get(int(id))
        if x == None:
            x = Admin.query.get(int(id))
        return x
    
    return app

def create_database(app):
    if not path.exists('website/database.db'):
        with app.app_context():
            db.create_all()
            print("created database")