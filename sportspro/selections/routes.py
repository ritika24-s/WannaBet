import os
import traceback
from flask import Blueprint, request, jsonify, abort

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
        if not request.get_json():
            abort(400, "Invalid input: No data provided")
        status_code, message = selection_views.create_selection(request.get_json())
        if status_code == 201:
            return jsonify({"id": int(message)}), 201
        if status_code>=400:
            return jsonify({"error_message": message}), status_code
    
    except Exception as e:
        logger.error(f"Error creating selection: {e}")
        return jsonify({'error': 'Failed to create selection'}), 500

# Endpoint to update an existing selection
@selections_bp.route('/<int:selection_id>', methods=["PUT", "PATCH"])
def update_selection(selection_id):
    try:
        data = request.get_json(force=True)
        status_code, message = selection_views.update_selection(int(selection_id), data)
        if status_code == 200:
            return jsonify({"id": int(selection_id)}), 200
        if status_code>=400:
            return jsonify({"error_message": message}), status_code
    except ValueError as e:
        logger.error(f"ValueError: {e}")
        abort(400, str(e))
    except KeyError as e:
        logger.error(f"KeyError: {e}")
        traceback.print_exc()
        abort(404, str(e))
    except Exception as e:
        logger.error(f"Error updating/deleting sport: {e}")
        abort(500, "Internal Server Error")

# Endpoint to search for selections based on specified criteria
@selections_bp.route('/search', methods=["POST"])
def search_selections():
    try:
        filters = request.get_json()
        status_code, selections = selection_views.search_selection(filters)

        if selections:
            return jsonify({'selections': selections}), 200
        return jsonify({"error_message": "No data found for the given filters"}), 404
    except Exception as e:
        logger.error(f"Error searching selections: {e}")
        return jsonify({'error': 'Failed to search selections'}), 500