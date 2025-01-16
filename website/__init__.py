from flask import Flask
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key_here'

    # Flask-Login setup
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    # Register blueprints or routes here
    from .routes import main
    app.register_blueprint(main)

    return app