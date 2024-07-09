# import pytest
# from sportspro import create_app
# from sportspro.db import DB

# @pytest.fixture(scope='module')
# def test_client():
#     flask_app = create_app()
#     flask_app.testing = True

#     # Flask provides a way to test your application by exposing the Werkzeug test Client 
#     # and handling the context locals for you.
#     with flask_app.test_client() as testing_client:
#         with flask_app.app_context():
#             yield testing_client

# @pytest.fixture(scope='module')
# def init_database():
#     db = DB()
#     db.execute_query("DELETE FROM sports;")
#     db.execute_query("ALTER TABLE sports AUTO_INCREMENT = 1;")
#     yield db
#     # db.execute_query("DELETE FROM sports;")
#     # db.execute_query("ALTER TABLE sports AUTO_INCREMENT = 1;")
