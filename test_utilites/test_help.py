import random
import string
import json,requests
from website import sent_to_server


key = "NEDD"


def id_generator(size=7, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def register(client, username, password, type_of_user,Email):
    return client.post('/handle_data', data=dict(
        Register_New_User=username,
        Register_New_Password=password,
        permissions=type_of_user,
        Email=Email,
        type_form='register'
    ), follow_redirects=True)


def change_password(client, oldpassword, newpassword):
    return client.post('/handle_data', data=dict(
        OldPassword=oldpassword,
        Password=newpassword,
        type_form='changePassword'
    ), follow_redirects=True)


def delete_from_sql(username):
    data = {'user': username}
    sent_to_server(data,"Testsingup")



def login(client, username, password):
    return client.post('/handle_data', data=dict(
        inputIdMain=username,
        inputPasswordMain=password,
        type_form='login'

    ), follow_redirects=True)


def update_permission_in_sql(username, authority):
    data = {'UserUpdate': username, 'Permissions': authority, 'User': 'admin'}
    return sent_to_server(data, "SetPermissions")



def logout(client):
    return client.get('/logout', follow_redirects=True)

