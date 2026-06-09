import pytest
import requests
import json

# Base URL for API
base_url = 'http://localhost:8000'

# Positive test: Valid request payload returning expected success code
def test_create_pet_positive():
    payload = {'name': 'Test Pet'}
    response = requests.post(f'{base_url}/pets', json=payload)
    assert response.status_code == 201

# Negative tests
def test_create_pet_negative_missing_required_field():
    payload = {}
    response = requests.post(f'{base_url}/pets', json=payload)
    assert response.status_code != 201

def test_create_pet_negative_invalid_data_type():
    payload = {'name': 123}
    response = requests.post(f'{base_url}/pets', json=payload)
    assert response.status_code != 201

# Boundary tests
def test_create_pet_boundary_empty_string():
    payload = {'name': ''}
    response = requests.post(f'{base_url}/pets', json=payload)
    assert response.status_code != 201

def test_create_pet_boundary_max_length():
    payload = {'name': 'a' * 1000}
    response = requests.post(f'{base_url}/pets', json=payload)
    assert response.status_code == 201

def test_create_pet_boundary_null_value():
    payload = {'name': None}
    response = requests.post(f'{base_url}/pets', json=payload)
    assert response.status_code != 201

# Test with null payload
def test_create_pet_null_payload():
    response = requests.post(f'{base_url}/pets', json=None)
    assert response.status_code != 201

# Test with invalid JSON payload
def test_create_pet_invalid_json_payload():
    response = requests.post(f'{base_url}/pets', data='Invalid JSON')
    assert response.status_code != 201