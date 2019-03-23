import random
import string


def id_generator(size=7, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def register(client, username, password, type_of_user):
    return client.post('/handle_data', data=dict(
        Register_New_User=username,
        Register_New_Password=password,
        permissions=type_of_user,
        type_form='register'
    ), follow_redirects=True)


def change_password(client, oldpassword, newpassword):
    return client.post('/handle_data', data=dict(
        OldPassword=oldpassword,
        Password=newpassword,
        type_form='changePassword'
    ), follow_redirects=True)

