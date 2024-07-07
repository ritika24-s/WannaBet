import os
from flask import Flask
from dotenv import load_dotenv

from .config import *

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config_by_name[os.environ.get("FLASK_ENV", "development")])

    # import the routes
    from .routes import main, errors
    from .sports.routes import sports_bp
    from .events.routes import events_bp
    from .selections.routes import selections_bp

    # and register all blueprints
    app.register_blueprint(sports_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(selections_bp)

    return app
