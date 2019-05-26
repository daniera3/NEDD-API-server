from website import app
import test.test_help as th
import os
import tempfile
import pytest
import unittest



@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    client = app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def test_index(client):
    response = client.get('/')
    assert b'login' in response.data


def test_login_page(client):
    response = client.get('/login')
    assert b'login' in response.data


# see if admin user can log in and log out
class AdminRegister(unittest.TestCase):
    client = app.test_client()

    @classmethod
    def setUpClass(cls):
        app.config['USERNAME'] = th.id_generator()
        app.config['PASSWORD'] = th.id_generator()
        th.register(cls.client, app.config['USERNAME'], app.config['PASSWORD'], 'normal',"danidani@gmail.com")

    def test_admin(self):
        answer = th.update_permission_in_sql(app.config['USERNAME'], 'Admin')
        assert  answer['status'] == 'success'
        print(answer)
        rv = th.login(self.client, app.config['USERNAME'], app.config['PASSWORD'])
        assert b'enter key sender to your email' in rv.data

    @classmethod
    def tearDownClass(cls):
        th.logout(cls.client)
        th.delete_from_sql(app.config['USERNAME'])


# try to register new user and then change his password
class TestRegisterAndChangePassword(unittest.TestCase):
    client = app.test_client()

    @classmethod
    def setUpClass(cls):
        app.config['USERNAME'] = th.id_generator()
        app.config['PASSWORD'] = th.id_generator()
        app.config['NEWPASSWORD'] = th.id_generator()

    def test_change_password(self):
        rv = th.register(self.client, app.config['USERNAME'], app.config['PASSWORD'], 'normal', "danidain@gmail.com")
        print("register new user")
        assert b'{}',(app.config['USERNAME'],) in rv.data

        th.change_password(self.client, app.config['PASSWORD'], app.config['NEWPASSWORD'])
        th.logout(self.client)
        rv = th.login(self.client, app.config['USERNAME'], app.config['NEWPASSWORD'])
        print("try to log in with new password")
        assert b'enter key sender to your email' in rv.data

    @classmethod
    def tearDownClass(cls):
        th.logout(cls.client)
        th.delete_from_sql(app.config['USERNAME'])


class TestRequestAccesptAndDenide(unittest.TestCase):
    client = app.test_client()

    @classmethod
    def setUpClass(cls):
        app.config['USERNAME'] = th.id_generator()
        app.config['PASSWORD'] = th.id_generator()
        th.register(cls.client, app.config['USERNAME'], app.config['PASSWORD'], 'normal',"danidani@gmail.com")
        th.update_permission_in_sql(app.config['USERNAME'], 'Admin')

    @pytest.mark.run(order=1)
    def test_deny_admin_request(self):

        pass

    @classmethod
    def tearDownClass(cls):
        th.delete_from_sql(app.config['USERNAME'])

#TODO creath log in test
class TestLogIn(unittest.TestCase):
    client = app.test_client()

    @classmethod
    def setUpClass(cls):
        app.config['USERNAME'] = th.id_generator()
        app.config['PASSWORD'] = th.id_generator()

        th.register(cls.client, app.config['USERNAME'], app.config['PASSWORD'], 'normal',"danidani@gmail.com")
        th.update_permission_in_sql(app.config['USERNAME'], 'Admin')

    @pytest.mark.run(order=1)
    def test_deny_admin_request(self):

        pass

    @classmethod
    def tearDownClass(cls):
        th.delete_from_sql(app.config['USERNAME'])

