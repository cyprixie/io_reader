''' unit tests for the server endpoints in the `src.server` module.

The tests include scenarios for the `/counter_state` endpoint, 
which retrieves the counter state for a given process ID.
'''

import os
import pytest
from src.server import app

# proc/1/io valid file content
# proc/2/io wrong value type
# proc/3/io permission denied
# proc/4/io missing the write_bytes key

@pytest.fixture(name="client")
def test_client():
    """
    A context manager that provides a test client for the Flask application.
    """

    app.config['TESTING'] = True
    os.environ['FILE_PATH'] = './test/proc/%i/io'
    with app.test_client() as client:
        yield client

def test_counter_state(client):
    """
    Test the counter state endpoint with different scenarios.
    """

    # Test case 1: Valid process ID
    response = client.get('/counter_state/1')
    assert response.status_code == 200
    assert response.get_json() == {'write_bytes': 1, 'read_bytes': 2}

    # Test case 2: Non-existent process ID
    response = client.get('/counter_state/456')
    assert response.status_code == 404

    # TODO: Pre steps needed to setup a file without read permissions  # pylint: disable=fixme
    # Test case 3: Permission denied
    # response = client.get('/counter_state/3')
    # assert response.status_code == 403

    # Test case 4: Invalid content
    response = client.get('/counter_state/2')
    assert response.status_code == 422

    # Test case 5: Missing write_bytes key
    response = client.get('/counter_state/4')
    assert response.status_code == 422
