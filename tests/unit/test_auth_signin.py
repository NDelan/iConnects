from app import create_app
import os

def test_signin_page(test_client):   
    """
    GIVEN a Flask application configured for testing    
    WHEN the '/login' page is requested (GET)    
    THEN check the response is valid    
    """    
    response = test_client.get('/signin')
    assert response.status_code == 200
    assert b'username' in response.data
    assert b'password' in response.data


def test_signup_page(test_client):
    """
    GIVEN a Flask application configured for testing    
    WHEN the '/login' page is requested (GET)    
    THEN check the response is valid    
    """    
    response = test_client.get('/signup')
    assert response.status_code == 200
    assert b'firstname' in response.data
    assert b'lastname' in response.data
    assert b'email' in response.data
    assert b'password' in response.data


