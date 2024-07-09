import pytest
import json

def test_create_sport(test_client, init_database):
    """
    Test creating a new sport.
    """
    sport_data = {
        "name": "Soccer",
        "slug": "soccer",
        "active": True
    }
    response = test_client.post('/sport/', data=json.dumps(sport_data), content_type='application/json')
    assert response.status_code == 201
    assert 'id' in response.json

def test_create_duplicate_sport(test_client):
    """
    Test creating a duplicate sport (should fail).
    """
    sport_data = {
        "name": "Soccer",
        "slug": "soccer",
        "active": True
    }
    response = test_client.post('/sport/', data=json.dumps(sport_data), content_type='application/json')
    assert response.status_code == 409

def test_update_sport(test_client):
    """
    Test updating an existing sport.
    """
    updated_data = {
        "name": "Football",
        "slug": "football",
        "active": False
    }
    response = test_client.patch('/sport/1', data=json.dumps(updated_data), content_type='application/json')
    assert response.status_code == 200
    assert response.json['id'] == 1

def test_delete_sport(test_client):
    """
    Test deleting an existing sport.
    """
    response = test_client.delete('/sport/1', data=json.dumps({}), content_type='application/json')
    assert response.status_code == 200
    assert response.json['id'] == 1

def test_get_all_sports(test_client):
    """
    Test retrieving all sports.
    """
    response = test_client.get('/sport/', content_type='application/json')
    assert response.status_code == 200
    assert isinstance(response.json['sports'], list)

def test_search_sport(test_client):
    """
    Test searching for sports based on filters.
    """
    # Create a sport for search
    sport_data = {
        "name": "Basketball",
        "slug": "basketball",
        "active": True
    }
    test_client.post('/sport/', data=json.dumps(sport_data), content_type='application/json')

    search_data = {
        "name": "Basketball",
        "active": True
    }
    response = test_client.post('/sport/search', data=json.dumps(search_data), content_type='application/json')
    assert response.status_code == 200
    assert len(response.json['sports']) > 0
    assert response.json['sports'][0]['name'] == "Basketball"
