import os
from flask import Flask

from .sports import routes

from .selections import routes

from .events import routes

from .config import *

app = Flask(__name__)
app.config.from_object(config_by_name[os.environ.get("FLASK_ENV", "development")])

# import the routes
from .routes import main, errors

# and register all blueprints
app.register_blueprint(routes.events_bp)
app.register_blueprint(routes.sports_bp)
app.register_blueprint(routes.selections_bp)
