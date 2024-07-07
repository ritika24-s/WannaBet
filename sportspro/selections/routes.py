import os
from flask import Blueprint, request, jsonify

# from sportspro import app
from ..utils.logger import setup_logger
from ..config import config_by_name
from .views import SelectionsViews

config = config_by_name[os.getenv('FLASK_ENV', 'development')]
logger = setup_logger(config.LOG_LEVEL)

# Create a selections blueprint
selections_bp = Blueprint('selections', __name__, url_prefix='/selections')
selection_views = SelectionsViews()

# Endpoint to create a new selection
@selections_bp.route('/', methods=["POST"])
def create_selection():
    try:
        data = request.get_json()
        selection_id = selection_views.create_selection(data)
        return jsonify({'id': selection_id}), 201
    except Exception as e:
        logger.error(f"Error creating selection: {e}")
        return jsonify({'error': 'Failed to create selection'}), 500

# Endpoint to update an existing selection
@selections_bp.route('/<selection_id>', methods=["UPDATE"])
def update_selection(selection_id):
    try:
        data = request.get_json()
        updated_selection_id = selection_views.update_selection(selection_id, data)
        return jsonify({'id': updated_selection_id})
    except Exception as e:
        logger.error(f"Error updating selection: {e}")
        return jsonify({'error': 'Failed to update selection'}), 500

# Endpoint to search for selections based on specified criteria
@selections_bp.route('/search', methods=["POST"])
def search_selections():
    try:
        filters = request.get_json()
        selections = selection_views.search_selections(filters)
        return jsonify({'selections': selections})
    except Exception as e:
        logger.error(f"Error searching selections: {e}")
        return jsonify({'error': 'Failed to search selections'}), 500