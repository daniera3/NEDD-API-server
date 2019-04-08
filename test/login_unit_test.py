import website
import unittest
import test.test_help as th


class TestLogIn(unittest.TestCase):
    username = None
    password = None
    email = None
    data = None

    def setUp(self):
        self.username = th.id_generator()
        self.password = th.id_generator()
        self.email = th.id_generator() + "@" + th.id_generator()
        data = {'User': self.username, 'Password': self.password, 'perm': "normal", 'Email': self.email}
        website.sent_to_server(data, "singup")

    def test_server_login(self):
        data = {'user': self.username, 'pas': self.password}
        result = website.sent_to_server(data, "singin")
        assert result['status'] == "success"
        assert result['permissions'] == "normal"

    def test_server_login_wrong_password(self):
        data = {'user': self.username, 'pas': th.id_generator()}
        result = website.sent_to_server(data, "singin")
        assert result['status'] == "Pfail"

    def test_server_login_wrong_username(self):
        data = {'user': th.id_generator(), 'pas': self.password}
        result = website.sent_to_server(data, "singin")
        assert result['status'] == "Ufail"

    def test_server_login_without_username(self):
        data = {'pas': self.password}
        result = website.sent_to_server(data, "singin")
        assert result['status'] == "fail"

    def tearDown(self):
        data = {'user': self.username}
        website.sent_to_server(data, "Testsingup")
