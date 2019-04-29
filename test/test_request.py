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

        # creath new request
        data = {'user': self.username_admin,
                'UserName': self.username,
                'ReasonForRequest': "test"}
        website.sent_to_server(data, "RequestPermissions")
        # accept the requset

        data = {'User': self.username_admin,
                'requesting': self.username_admin,
                'user': self.username,
                'insert': True}
        website.sent_to_server(data, "AdminAnswers")




    def tearDown(self):
        data = {'user': self.username}
        website.sent_to_server(data, "Testsingup")
        data = {'user': self.username_admin}
        website.sent_to_server(data, "Testsingup")

    def test_get_student_list(self):
        data = {'UserRequsting': self.username_admin}
        result = website.sent_to_server(data, "getstudents")
        assert result['status'] == 'success'
        assert self.username in result['data']





