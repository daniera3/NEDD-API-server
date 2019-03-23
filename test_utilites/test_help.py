import random
import string
import json,requests


key = "NEDD"


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


def delete_from_sql(username):
    data = {'user': username}
    data = json.dumps(data)
    header = {"Content-Type": "application/json"}
    requests.post('https://asqwzx1.pythonanywhere.com/Testsingup', auth=('asqwzx1', 'NEDD'), data=data, headers=header)


def login(client, username, password):
    return client.post('/handle_data', data=dict(
        inputIdMain=username,
        inputPasswordMain=password,
        type_form='login'

    ), follow_redirects=True)


def update_permission_in_sql(username, authority):
    data = {'UserUpdate': username, 'Permissions': authority, 'User': 'admin'}
    data = json.dumps(data)
    header = {"Content-Type": "application/json"}
    response = requests.post('https://asqwzx1.pythonanywhere.com/SetPermissions', auth=('asqwzx1', 'NEDD'), data=data,
                  headers=header)
    return response


def logout(client):
    return client.get('/logout', follow_redirects=True)

