import pytest
from flask import Flask

from sportspro import create_app
from ..db.init_db import CreateSchema
from ..config import *

@pytest.fixture
def app():
    app = create_app()
    app.config.from_object(DevelopmentConfig)
    create_schema = CreateSchema()
    create_schema.init_db()

    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

def test_app_exists(client):
    response = client.get("/")
    assert response.status_code == 404