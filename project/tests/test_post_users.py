import pytest
import requests
import json

# Base URL
base_url = 'http://localhost:8000'

# Positive test case: Valid request payload
def test_create_user_positive():
    payload = {
        'name': 'John Doe',
        'email': 'johndoe@example.com'
    }
    response = requests.post(base_url + '/users', json=payload)
    assert response.status_code == 201

# Negative test cases
def test_create_user_negative_missing_name():
    payload = {
        'email': 'johndoe@example.com'
    }
    response = requests.post(base_url + '/users', json=payload)
    assert response.status_code == 400

def test_create_user_negative_missing_email():
    payload = {
        'name': 'John Doe'
    }
    response = requests.post(base_url + '/users', json=payload)
    assert response.status_code == 400

def test_create_user_negative_invalid_email():
    payload = {
        'name': 'John Doe',
        'email': 'invalid_email'
    }
    response = requests.post(base_url + '/users', json=payload)
    assert response.status_code == 400

def test_create_user_negative_invalid_name():
    payload = {
        'name': 123,
        'email': 'johndoe@example.com'
    }
    response = requests.post(base_url + '/users', json=payload)
    assert response.status_code == 400

# Boundary test cases
def test_create_user_boundary_empty_name():
    payload = {
        'name': '',
        'email': 'johndoe@example.com'
    }
    response = requests.post(base_url + '/users', json=payload)
    assert response.status_code == 400

def test_create_user_boundary_empty_email():
    payload = {
        'name': 'John Doe',
        'email': ''
    }
    response = requests.post(base_url + '/users', json=payload)
    assert response.status_code == 400

def test_create_user_boundary_max_length_name():
    payload = {
        'name': 'a' * 1000,
        'email': 'johndoe@example.com'
    }
    response = requests.post(base_url + '/users', json=payload)
    assert response.status_code == 400

def test_create_user_boundary_max_length_email():
    payload = {
        'name': 'John Doe',
        'email': 'a' * 1000 + '@example.com'
    }
    response = requests.post(base_url + '/users', json=payload)
    assert response.status_code == 400

def test_create_user_boundary_null_name():
    payload = {
        'name': None,
        'email': 'johndoe@example.com'
    }
    response = requests.post(base_url + '/users', json=payload)
    assert response.status_code == 400

def test_create_user_boundary_null_email():
    payload = {
        'name': 'John Doe',
        'email': None
    }
    response = requests.post(base_url + '/users', json=payload)
    assert response.status_code == 400