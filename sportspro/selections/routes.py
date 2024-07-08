import os
from flask import Blueprint, request, jsonify

from .views import SelectionsViews
from ..utils.logger import get_logger

logger = get_logger(__name__)

# Create a selections blueprint
selections_bp = Blueprint('selection', __name__, url_prefix='/selection')
selection_views = SelectionsViews()

# Endpoint to create a new selection
@selections_bp.route('/', methods=["POST"])
def create_selection():
    try:
        selection_id = selection_views.create_selection(request.get_json())
        return jsonify({'id': selection_id}), 201
    except Exception as e:
        logger.error(f"Error creating selection: {e}")
        return jsonify({'error': 'Failed to create selection'}), 500

# Endpoint to update an existing selection
@selections_bp.route('/<int:selection_id>', methods=["UPDATE"])
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