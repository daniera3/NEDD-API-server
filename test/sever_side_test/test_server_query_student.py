import unittest
import server_side.server as sr
import test.test_help as th


class TestSerchUser_server_query(unittest.TestCase):
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



    def tearDown(self):
        data = {'user': self.username_admin}
        result = th.sent_to_server_local(self.client_server, data, "Testsingup")
        assert result['status'] == 'success'


    def test_server_get_student_data(self):
        '''data = {'UserRequsting': self.username_admin,'serchData': self.username_admin}
        result = th.sent_to_server_local(self.client_server, data, "getstudentsQuery")
        print(result)'''
        assert 1==1









