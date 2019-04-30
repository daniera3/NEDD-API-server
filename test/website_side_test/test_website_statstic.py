import website
import unittest
import test.test_help as th
from werkzeug.security import generate_password_hash


class TestStatisticWebsite(unittest.TestCase):
    username_admin = None
    password_admin = None
    email_admin = None
    username = None
    password = None
    email = None
    app = None
    client_website = None

    def setUp(self):
        print("start set up process")
        self.app = website.Flask(__name__)
        website.app.config.from_object('config.TestingConfig')
        self.client_website = website.app.test_client()
        print("finish set up web client")
        self.username_admin = th.id_generator()
        self.password_admin = th.id_generator()
        self.email_admin = th.id_generator() + "@" + th.id_generator()

        result = website.register(self.username_admin,
                         generate_password_hash(self.password_admin,method='pbkdf2:sha256', salt_length=50),
                         "normal",
                         self.email_admin)
        assert result is True
        print("the user "+self.username_admin+" got register")

        data = {'User': 'admin', 'UserUpdate': self.username_admin, 'Permissions': "Admin"}
        result = website.sent_to_server(data, "SetPermissions")
        assert result['status'] == 'success'
        print("the user " + self.username_admin + " is admin")

        self.username = th.id_generator()
        self.password = th.id_generator()
        self.email = th.id_generator() + "@" + th.id_generator()

        result = website.register(self.username,
                                  generate_password_hash(self.password, method='pbkdf2:sha256', salt_length=50),
                                  "normal",
                                  self.email)
        assert result is True
        print("the user " + self.username + " got register")

        data = {'user': self.username_admin,
                'UserName': self.username,
                'ReasonForRequest': "test"}
        result = website.sent_to_server(data, "RequestPermissions")
        assert result['status'] == 'success seve request'
        print("the user " + self.username_admin + " is asking for responsibility for "+self.username)
        # accept the requset

        data = {'User': self.username_admin,
                'requesting': self.username_admin,
                'user': self.username,
                'insert': True}

        result = website.sent_to_server(data, "AdminAnswers")
        assert result['status'] == 'deleted this request and saved'
        print("the user " + self.username_admin + " is responsible for " + self.username)

    def tearDown(self):
        print("start tear down")
        data = {'user': self.username}
        result = website.sent_to_server(data, "Testsingup")
        assert result['status'] == 'success'
        print("deleted "+self.username)
        data = {'user': self.username_admin}
        result = website.sent_to_server(data, "Testsingup")
        assert result['status'] == 'success'
        print("deleted " + self.username_admin)

    def test_server_get_student_list(self):
        print("--- testing  test_server_get_student_list ---")
        print("try to login ")
        result = th.login(self.client_website, self.username_admin, self.password_admin)

        self.assertIn(bytes(self.username_admin, "utf-8"), result.data)
        print("login successfully")

