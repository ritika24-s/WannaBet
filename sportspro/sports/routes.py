from flask import Blueprint, request, jsonify, abort

# from sportspro import app
from .views import SportsViews


# Create a sports blueprint
sports_bp = Blueprint('sport', __name__, url_prefix="/sport")
sports_views = SportsViews()

# Endpoint to create a new sport.
@sports_bp.route('/', methods=["POST"])
def create_new_sport():
    try:
        status_code, message = sports_views.create_sport(data=request.get_json())
        if status_code == 201:
            return jsonify({"id": int(message)}), 201
        else:
            abort(status_code, message)
    except Exception as e:
        abort(500, str(e))

# Endpoint to update an existing sport
@sports_bp.route('/<sport_id>', methods=["UPDATE"])
def update_sport(sport_id):
    try:
        status_code, message = sports_views.update_sport(sport_id, request.get_json())
        if status_code == 200:
            return jsonify({"id": int(sport_id)}), 200
        else:
            abort(status_code, message)

    except ValueError as e:
        abort(400, str(e))
    except KeyError as e:
        abort(404, str(e))
    except Exception as e:
        abort(500, str(e))
    
# Endpoint to delete an existing sport
@sports_bp.route('/<sport_id>', methods=["DELETE"])
def delete_sport(sport_id):
    try:
        message, status_code = sports_views.delete_sport(sport_id=int(sport_id))
        print(status_code)
        if status_code == 200:
            return jsonify({'id':sport_id}), 200
        abort(status_code, message)
    
    except ValueError as e:
        abort(400, str(e))
    except KeyError as e:
        abort(404, str(e))
    except Exception as e:
        abort(500, str(e))

# Endpoint to search for sports based on specified criteria
@sports_bp.route('/search', methods=["POST"])
def search_particular_sport(): 
    try:
        sports = sports_views.search_sport(request.get_json())
        if sports:
            return jsonify({"sports": sports}), 200
        abort(404, "No data found for the given filters")
    
    except Exception as e:
        abort(500, str(e))