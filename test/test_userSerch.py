import website
import unittest
import test.test_help as th


class TestSerchUser(unittest.TestCase):
    username_admin = None
    password_admin = None
    email_admin = None
    username = None
    password = None
    email = None

    def setUp(self):
        self.username_admin = th.id_generator()
        self.password_admin = th.id_generator()
        self.email_admin = th.id_generator() + "@" + th.id_generator()
        data = {'User': self.username_admin, 'Password': self.password_admin, 'perm': "normal",
                'Email': self.email_admin}
        website.sent_to_server(data, "singup")
        data = {'User': 'admin', 'UserUpdate': self.username_admin, 'Permissions': "Admin"}
        website.sent_to_server(data, "SetPermissions")
        self.username = th.id_generator()
        self.password = th.id_generator()
        self.email = th.id_generator() + "@" + th.id_generator()
        data = {'User': self.username, 'Password': self.password, 'perm': "normal", 'Email': self.email}
        website.sent_to_server(data, "singup")

    def tearDown(self):
        data = {'user': self.username}
        website.sent_to_server(data, "Testsingup")
        data = {'user': self.username_admin}
        website.sent_to_server(data, "Testsingup")

    def test_get_user_to_delete(self):
        data = {'User': self.username_admin}
        result = website.sent_to_server(data, "GetUsersToDelete")
        assert result['status'] == 'success'
        for user in result['data']:
            if user['User'] == self.username:
                pass

    def test_get_user_to_delete_user_not_admin(self):
        data = {'User': th.id_generator()}
        result = website.sent_to_server(data, "GetUsersToDelete")
        assert result['status'] == 'haven\'t Permissions'

    def test_get_user_not_inside(self):
        data = {'User': self.username_admin}
        result = website.sent_to_server(data, "GetUsersToDelete")
        assert result['status'] == 'success'
        for user in result['data']:
            if user['User'] == th.id_generator():
                assert 1 == 2
        pass

    def test_get_user_in_delete(self):
        data = {'User': self.username_admin, 'del': self.username}
        result = website.sent_to_server(data, "DeleteUser")
        assert result['status'] == 'success'
        result = website.sent_to_server(data, "GetUsersToReturn")
        for user in result['data']:
            if user['User'] == self.username:
                pass

    def test_get_user_to_return_user_not_admin(self):
        data = {'User': th.id_generator()}
        result = website.sent_to_server(data, "GetUsersToReturn")
        assert result['status'] == 'haven\'t Permissions'

    def test_get_user_not_inside_delete(self):
        data = {'User': self.username_admin, 'del': self.username}
        result = website.sent_to_server(data, "DeleteUser")
        assert result['status'] == 'success'
        data = {'User': self.username_admin}
        result = website.sent_to_server(data, "GetUsersToReturn")
        assert result['status'] == 'success'
        for user in result['data']:
            if user['User'] == th.id_generator():
                assert 1 == 2
        pass

    def test_get_delete_and_return(self):
        data = {'User': self.username_admin, 'del': self.username}
        result = website.sent_to_server(data, "DeleteUser")
        assert result['status'] == 'success'
        result = website.sent_to_server(data, "GetUsersToReturn")
        for user in result['data']:
            if user['User'] == self.username:
                pass
        data = {'User': self.username_admin, 'ReturnU': self.username}
        result = website.sent_to_server(data, "ReturnUser")
        assert result['status'] == 'success'
        self.test_get_user_to_delete()

