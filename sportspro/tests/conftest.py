import pytest
from sportspro import create_app
from sportspro.db.init_db import CreateSchema
from sportspro.db import DB

@pytest.fixture(scope="module")
def app():
    app = create_app()
    app.config["TESTING"] = True
    # db = CreateSchema()
    # db.del_db()
    # db.init_db()

    return app

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

@pytest.fixture(scope='module')
def runner(app):
    return app.test_cli_runner()