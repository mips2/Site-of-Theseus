from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Load configuration from environment variables
    app.config.from_prefixed_env()
    
    # Register blueprints or routes here
    from .routes import main
    app.register_blueprint(main)
    
    return app