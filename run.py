#!/usr/bin/env python3

from flask import Flask
from auth import login_manager, load_user
from routes import main as main_blueprint
from extensions import db, migrate, login, bcrypt, csrf, socketio
from config import Config

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)
    socketio.init_app(app)

    login.login_view = 'main.login'


    app.register_blueprint(main_blueprint)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
