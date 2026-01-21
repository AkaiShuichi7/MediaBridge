import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    # Ensure instance path is explicitly set to backend/instance
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    instance_path = os.path.join(base_dir, 'instance')
    
    app = Flask(__name__, instance_path=instance_path)
    app.config.from_object(config_class)

    # Ensure instance directory exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    db.init_app(app)
    CORS(app)

    # Register blueprints
    from .api.routes import bp as api_bp
    app.register_blueprint(api_bp)
    
    # Create tables
    with app.app_context():
        # Import models to ensure they are registered
        from .models import user, task
        db.create_all()

    return app
