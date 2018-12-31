#import statements
import pytest
from flask import current_app
from ...app.models import User

def test_app_exists(flask_app):
    assert current_app is not None

def test_app_is_testing(flask_app):
    assert current_app.config['TESTING'] is True

def test_hello(flask_client):
    response = flask_client.get('/')
    assert response.status_code == 200

def test_password_setter():
    u = User(password = 'cat')
    assert u.password_hash is not None

def test_no_password_getter():
    u = User(password= 'cat')
    with pytest.raises(AttributeError):
        u.password

def test_password_salts_are_random():
    u = User(password='cat')
    u2 = User(password='cat')
    assert u.password_hash != u2.password_hash