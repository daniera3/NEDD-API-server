import unittest

from website import app
import os
import tempfile
import pytest


@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def test_login_logout(client):
    response = client.get('/')
    assert b'login' in response.data


