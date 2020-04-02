# tests/conftest.py
import pytest
import json

def pytest_configure(config):
    config.addinivalue_line("markers", "e2e: mark as end-to-end test.")


@pytest.fixture
def mock_requests_get(mocker):
    mock = mocker.patch("requests.get")
    with open('tests/mocks/search_response.json') as json_file:
        search_response = json.load(json_file)
        mock.return_value.__enter__.return_value.json.return_value = search_response
        return mock