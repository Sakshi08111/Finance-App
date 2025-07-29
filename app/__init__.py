from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    """
    Factory function to create and configure the Flask application.
    """
    # Create the Flask application instance
    app = Flask(__name__)

    # Configure the application
    app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Configure Flask-Login
    login_manager.login_view = 'routes.auth'  # Ensure this matches your route's endpoint
    login_manager.login_message_category = 'info'  # Optional: Style for login messages

    # Register blueprints
    from .routes import routes
    app.register_blueprint(routes)

    # Import and register other parts of the application
    with app.app_context():
        # Import models to ensure they are registered with SQLAlchemy
        from . import models

        # Create database tables if they don't exist
        db.create_all()

    return app