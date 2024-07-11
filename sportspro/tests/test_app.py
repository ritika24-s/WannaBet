import pytest
from flask import Flask

from sportspro import create_app
from ..db.init_db import CreateSchema
from ..config import *
from sportspro.db import DB

@pytest.fixture()
def db(app):
    """
    DB fixture to reset DB for testing
    """
    # Initialize the database and create some initial test data
    db = DB()

    # delete data before tests
    db.execute_query("DELETE from selections;")
    db.execute_query("ALTER TABLE selections AUTO_INCREMENT = 1;")
    db.execute_query("DELETE from events;")
    db.execute_query("ALTER TABLE events AUTO_INCREMENT = 1;")
    db.execute_query("DELETE from sports;")
    db.execute_query("ALTER TABLE sports AUTO_INCREMENT = 1;")  
       
    # Insert initial data for testing
    db.execute_query(
        query="INSERT INTO sports (name, slug, active) VALUES (%s, %s, %s)",
        values=("Football", "football", True)
    )

    db.execute_query(
        "INSERT INTO events (name, slug, active, type, sport, status, scheduled_start, actual_start, logos) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        ("Arsenal vs Leeds", "arsenal-vs-leeds", True, "preplay", "Football", "PENDING", "2023-07-01 10:00:00", None, None)
    )

    db.execute_query(
        "INSERT INTO selections (name, event, active, price, outcome) VALUES (%s, %s, %s, %s, %s)",
        ("Draw", "Arsenal vs Leeds", False, 100, "UNSETTLED")
    )

    yield db


    # # delete data after tests

    # db.execute_query("DELETE FROM sports;")
    # db.execute_query("ALTER TABLE sports AUTO_INCREMENT = 1;")
    # db.execute_query("DELETE from events;")
    # db.execute_query("ALTER TABLE events AUTO_INCREMENT = 1;")
    # db.execute_query("DELETE from selections;")
    # db.execute_query("ALTER TABLE selections AUTO_INCREMENT = 1;")

def test_app_exists(client, db):
    response = client.get("/")
    assert response.status_code == 404