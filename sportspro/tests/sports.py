import pytest
from sportspro.sports.models import SportsModels
from db import DB 
from ..config import Config

@pytest.fixture
def sportsdb():
    sportsdb = SportsModels(Config)
    return sportsdb

def test_add_new_sports(sportsdb):
    sport = {
    "name": "Rugby",
    "slug": "rugby",
    "active": True
    }
    sportsdb.create_sport(sport)


def test_update_sport():
    sport = {
    "name": "Rugby",
    "slug": "rugby",
    "active": False
    }
    
def test_get_sport():
    search_data = {
    "name": "Football",
    "active": True
}