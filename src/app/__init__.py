from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
#from flask_login import LoginManager


# To implement Google Cloud Logging
from app.glog_manager import GoogleCloudLogManager

#login = LoginManager()
bootstrap = Bootstrap()
gl = GoogleCloudLogManager()


def create_app(config_class=Config):
    # Create Flask app
    app = Flask(__name__)

    # Load config
    app.config.from_object(config_class)

    # Initialize Bootstrap (HTML, CSS, JS)  manager
    bootstrap.init_app(app)

    # Initialize app logger
    gl.init_app(app)
    # Uncomment to log to Google Cloud on startup
    # Example for demo purposes
    gl.logging_example()

    # Flask blueprints imports
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    if not app.debug and not app.testing:
        # Extra initialization when testing or debugging
        pass

    return app
