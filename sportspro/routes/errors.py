from flask import jsonify
from sportspro import create_app
from ..utils.logger import get_logger

app = create_app()
logger = get_logger("error_routes")

@app.errorhandler(400)
def bad_request_error(error):
    logger.error(f"400 error: {error}")
    response = jsonify({'error': 'Bad Request', 'message': str(error)})
    response.status_code = 400
    return response

@app.errorhandler(404)
def not_found_error(error):
    logger.error(f"404 error: {error}")
    response = jsonify({'error': 'Not Found', 'message': str(error)})
    response.status_code = 404
    return response

@app.errorhandler(409)
def not_found_error(error):
    logger.error(f"409 error: {error}")
    response = jsonify({'error': 'Dupliacte entry', 'message': str(error)})
    response.status_code = 409
    return response

@app.errorhandler(500)
def internal_server_error(error):
    logger.error(f"500 error: {error}")
    response = jsonify({'error': 'Internal Server Error', 'message': str(error)})
    response.status_code = 500
    return response

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"500 error: {e}")
    response = jsonify({'error': 'Server Error', 'message': str(e)})
    response.status_code = 500
    return response
