import pytest
import requests

def test_get_pets():
    base_url = 'http://localhost:8000'
    endpoint = '/pets'
    url = base_url + endpoint
    response = requests.get(url)
    assert response.status_code == 200

def test_get_pets_invalid_url():
    base_url = 'http://localhost:8000'
    endpoint = '/invalid_pets'
    url = base_url + endpoint
    response = requests.get(url)
    assert response.status_code != 200

def test_get_pets_connection_refused():
    base_url = 'http://localhost:12345'
    endpoint = '/pets'
    url = base_url + endpoint
    with pytest.raises(requests.ConnectionError):
        requests.get(url)

def test_get_pets_timeout():
    base_url = 'http://localhost:8000'
    endpoint = '/pets'
    url = base_url + endpoint
    with pytest.raises(requests.Timeout):
        requests.get(url, timeout=0.001)

def test_get_pets_invalid_method():
    base_url = 'http://localhost:8000'
    endpoint = '/pets'
    url = base_url + endpoint
    response = requests.post(url)
    assert response.status_code != 200

def test_get_pets_empty_response():
    base_url = 'http://localhost:8000'
    endpoint = '/pets'
    url = base_url + endpoint
    response = requests.get(url)
    assert response.text is not None

def test_get_pets_headers():
    base_url = 'http://localhost:8000'
    endpoint = '/pets'
    url = base_url + endpoint
    response = requests.get(url)
    assert 'Content-Type' in response.headers

def test_get_pets_content_type():
    base_url = 'http://localhost:8000'
    endpoint = '/pets'
    url = base_url + endpoint
    response = requests.get(url)
    assert 'application/json' in response.headers.get('Content-Type')