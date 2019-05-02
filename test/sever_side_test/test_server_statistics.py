import unittest
import server_side.server as sr
import test.test_help as th
import random


class TestSerchUser_server(unittest.TestCase):
    username_admin = None
    password_admin = None
    email_admin = None
    username = None
    password = None
    email = None
    app = None
    client_server = None
    client_website = None

    def setUp(self):
        self.app = sr.Flask(__name__)
        self.app.config.from_object('config.TestingConfig')
        self.client_server = sr.app.test_client()

        self.username_admin = th.id_generator()
        self.password_admin = th.id_generator()
        self.email_admin = th.id_generator() + "@" + th.id_generator()
        data = {'User': self.username_admin, 'Password': self.password_admin, 'perm': "normal",
                'Email': self.email_admin}

        th.sent_to_server_local(self.client_server, data, "singup")

        data = {'User': 'admin', 'UserUpdate': self.username_admin, 'Permissions': "Admin"}
        th.sent_to_server_local(self.client_server, data, "SetPermissions")

        self.username = th.id_generator()
        self.password = th.id_generator()
        self.email = th.id_generator() + "@" + th.id_generator()
        data = {'User': self.username, 'Password': self.password, 'perm': "normal", 'Email': self.email}
        th.sent_to_server_local(self.client_server, data, "singup")

        # creath new request
        data = {'user': self.username_admin,
                'UserName': self.username,
                'ReasonForRequest': "test"}
        th.sent_to_server_local(self.client_server, data, "RequestPermissions")
        # accept the requset

        data = {'User': self.username_admin,
                'requesting': self.username_admin,
                'user': self.username,
                'insert': True}
        result = th.sent_to_server_local(self.client_server, data, "AdminAnswers")

    def tearDown(self):
        data = {'user': self.username}
        result = th.sent_to_server_local(self.client_server, data, "Testsingup")
        assert result['status'] == 'success'
        data = {'user': self.username_admin}
        result = th.sent_to_server_local(self.client_server, data, "Testsingup")
        assert result['status'] == 'success'

    def test_server_get_student_list(self):
        data = {'UserRequsting': self.username_admin}
        result = th.sent_to_server_local(self.client_server, data, "getstudents")
        assert result['status'] == 'success'
        assert self.username in result['data']

    def test_server_get_student_statistic(self):
        data = {'UserRequsting': self.username_admin}
        result = th.sent_to_server_local(self.client_server, data, 'getstudents')
        assert result['status'] == 'success'
        assert self.username in result['data']
        grade = random.randint(0, 10)
        data = {'user': self.username,
                'line': th.id_generator(),
                'say': th.id_generator(),
                'grade': grade
                }
        for i in range(5):
            result = th.sent_to_server_local(self.client_server, data, 'stest')
            assert result['status'] == 'save'

        data = {'user': self.username_admin,
                'user_search': self.username
                }
        result = th.sent_to_server_local(self.client_server, data, 'getStudentsStatistics')
        assert result['status'] == 'success'
        assert result['avrage'] == grade








