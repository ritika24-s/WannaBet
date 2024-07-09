import pytest
from sportspro import create_app


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    flask_app.config["TESTING"] = True

    # Flask provides a way to test your application by exposing the Werkzeug test Client 
    # and handling the context locals for you.
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client