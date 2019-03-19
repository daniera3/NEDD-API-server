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


def logout(client):
    return client.get('/logout', follow_redirects=True)


def test_index(client):
    response = client.get('/')
    assert b'login' in response.data


def test_login_page(client):
    response = client.get('/login')
    assert b'login' in response.data


def login(client, username, password):
    return client.post('/handle_data', data=dict(
        inputIdMain=username,
        inputPasswordMain=password,
        type_form='login'

    ), follow_redirects=True)


# see if admin user can log in and log out
def test_admin_login_logout(client):
    app.config['USERNAME'] = 'admin'
    app.config['PASSWORD'] = 'admin'

    rv = login(client, app.config['USERNAME'], app.config['PASSWORD'])
    assert b'Requset Users' in rv.data

    rv = logout(client)
    assert b'admin' not in rv.data

    rv = login(client, app.config['USERNAME'] + 'X', app.config['PASSWORD'])
    assert b'there was an error please try again' in rv.data

    rv = login(client, app.config['USERNAME'], app.config['PASSWORD'] + 'X')
    assert b'there was an error please try again' in rv.data


def register(client, username, password, type_of_user):
    return client.post('/handle_data', data=dict(
        Register_New_User=username,
        Register_New_Password=password,
        permissions=type_of_user,
        type_form='register'
    ), follow_redirects=True)


