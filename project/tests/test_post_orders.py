import pytest
import requests
import json

# Base URL for API
base_url = 'http://localhost:8000'

# Positive test: Valid request payload returning expected success code (201)
def test_create_order_positive():
    payload = {
        'user_id': 1,
        'item_name': 'Test Item',
        'quantity': 2
    }
    response = requests.post(base_url + '/orders', json=payload)
    assert response.status_code == 201

# Negative tests
def test_create_order_missing_required_fields():
    payload = {
        'item_name': 'Test Item',
        'quantity': 2
    }
    response = requests.post(base_url + '/orders', json=payload)
    assert response.status_code == 400

def test_create_order_invalid_data_types():
    payload = {
        'user_id': 'string',
        'item_name': 123,
        'quantity': 'string'
    }
    response = requests.post(base_url + '/orders', json=payload)
    assert response.status_code == 400

# Boundary tests
def test_create_order_empty_strings():
    payload = {
        'user_id': 1,
        'item_name': '',
        'quantity': 2
    }
    response = requests.post(base_url + '/orders', json=payload)
    assert response.status_code == 400

def test_create_order_max_length_values():
    payload = {
        'user_id': 1,
        'item_name': 'a' * 1000,
        'quantity': 2
    }
    response = requests.post(base_url + '/orders', json=payload)
    assert response.status_code == 400

def test_create_order_null_values():
    payload = {
        'user_id': None,
        'item_name': None,
        'quantity': None
    }
    response = requests.post(base_url + '/orders', json=payload)
    assert response.status_code == 400

def test_create_order_quantity_less_than_minimum():
    payload = {
        'user_id': 1,
        'item_name': 'Test Item',
        'quantity': 0
    }
    response = requests.post(base_url + '/orders', json=payload)
    assert response.status_code == 400

def test_create_order_quantity_non_integer():
    payload = {
        'user_id': 1,
        'item_name': 'Test Item',
        'quantity': 2.5
    }
    response = requests.post(base_url + '/orders', json=payload)
    assert response.status_code == 400

def test_create_order_user_id_non_integer():
    payload = {
        'user_id': 'string',
        'item_name': 'Test Item',
        'quantity': 2
    }
    response = requests.post(base_url + '/orders', json=payload)
    assert response.status_code == 400