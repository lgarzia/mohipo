#import statements
from flask import current_app

def test_app_exists(flask_app):
    assert current_app is not None

def test_app_is_testing(flask_app):
    assert current_app.config['TESTING'] is True

def test_hello(flask_client):
    response = flask_client.get('/')
    print(response.status_code)
    assert response.status_code == 200