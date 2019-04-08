import website
import unittest
import test.test_help as th


class TestRegister(unittest.TestCase):

    key = "NEDD"
    username = th.id_generator()
    password = th.id_generator()
    email = th.id_generator()+"@"+th.id_generator()

    def test_server_responds(self):
        data = {'user': "admin"}
        result = website.sent_to_server(data, "test")
        assert result['data'] == []

    def test_server_responds(self):
        data = {'user': "admin"}
        result = website.sent_to_server(data, "test")
        assert result['data'] is not None

    def test_server_register_normal(self):
        data = {'User': self.username, 'Password': self.password, 'perm': "normal", 'Email': self.email}
        result = website.sent_to_server(data, "singup")
        assert result['status'] == "success"
        data = {'user': self.username}
        result = website.sent_to_server(data, "Testsingup")
        assert result['status'] == "success"

    def test_server_register_hacker(self):
        data = {'User': self.username, 'Password': self.password, 'perm': th.id_generator(), 'Email': self.email}
        result = website.sent_to_server(data, "singup")
        assert result['status'] == "hacker"

    def test_server_register_premision(self):
        data = {'User': self.username, 'Password': self.password, 'Email': self.email}
        result = website.sent_to_server(data, "singup")
        assert result['status'] == "failAndCrash"

    def test_server_register_without_mail(self):
        data = {'User': self.username, 'Password': self.password, 'perm': "normal"}
        result = website.sent_to_server(data, "singup")
        assert result['status'] == "failAndCrash"

    def test_server_register_without_username(self):
        data = {'Email': self.email, 'Password': self.password, 'perm': "normal"}
        result = website.sent_to_server(data, "singup")
        assert result['status'] == "failAndCrash"

    def test_server_register_without_password(self):
        data = {'Email': self.email, 'Email': self.email, 'perm': "normal"}
        result = website.sent_to_server(data, "singup")
        assert result['status'] == "failAndCrash"

