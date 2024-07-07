from flask import jsonify
from sportspro import create_app

app = create_app()

@app.errorhandler(400)
def bad_request_error(error):
    response = jsonify({'error': 'Bad Request', 'message': str(error)})
    response.status_code = 400
    return response

@app.errorhandler(404)
def not_found_error(error):
    response = jsonify({'error': 'Not Found', 'message': str(error)})
    response.status_code = 404
    return response

@app.errorhandler(500)
def internal_server_error(error):
    response = jsonify({'error': 'Internal Server Error', 'message': str(error)})
    response.status_code = 500
    return response

@app.errorhandler(Exception)
def handle_exception(e):
    response = jsonify({'error': 'Server Error', 'message': str(e)})
    response.status_code = 500
    return response
