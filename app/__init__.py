import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from authlib.integrations.flask_client import OAuth


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.signin'  # Redirect to login page if not authenticated

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)


    # OAuth 2 client setup
    oauth = OAuth(app)
    google = oauth.register(
        name='google',
        client_id = app.config['GOOGLE_CLIENT_ID'],
        client_secret = app.config['GOOGLE_CLIENT_SECRET'],
        access_token_url = app.config['TOKEN_URI'],
        authorize_url = app.config['AUTH_URI'],
        api_base_url = app.config['API_BASE_URL'],
        client_kwargs={
            'scope': 'openid email profile',
        }
    )


    with app.app_context():
        from .auth.models import Student, Alum
        from .posts.models import Post
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        user = Alum.query.get(int(user_id))
        return user if user else Student.query.get(int(user_id))

    #blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .posts import posts as posts_blueprint
    app.register_blueprint(posts_blueprint)

    from .connections import connections as connections_blueprint
    app.register_blueprint(connections_blueprint)

    return app