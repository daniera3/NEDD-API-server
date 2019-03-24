from flask import Flask, render_template, request, session, url_for, redirect, json, flash
import requests
from os import urandom
from werkzeug.security import generate_password_hash, pbkdf2_hex
import Description
from sqlalchemy import create_engine
from flask_mail import Mail, Message
import os

'''   user autoriert
from flask_login import login_manager

from user_autorize import *
db.create_all()

admin_role =Role(name='ADMIN')
db.session.commit()
user1 = User(
    username='test', email='admin@example.com', active=True,
    password='test')
user1.roles = [admin_role]
db.session.commit()

login_manager = login_manager()
'''
app = Flask(__name__)



key = "NEDD"
#db in site for salt
db_connect = create_engine('sqlite:///nedd.db')



my_domain = 'asqwzx1.pythonanywhere.com/'
username = 'asqwzx1'
token = '973c7adaa1a72b549a6120af137ba68137ec2351'



app = Flask(__name__)

mail=Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'danirabinocivh123@gmail.com'
app.config['MAIL_PASSWORD'] = 'dani1212'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
app.secret_key = urandom(16)


def sendmail(header,email,massge):
    try:
        msg = Message(header, sender = 'danirabinocivh123@gmail.com', recipients = [email])
        msg.body = massge
        mail.send(msg)
        return "send"
    except:
        return "fill"

@app.route('/')
def index():
    if session.get('username'):
        if session['permissions'] == 'NORMAL':
            return render_template('status/normal_login.html')
        if session['permissions'] == 'MANGER':
            return render_template('status/parent_login.html')
        if session['permissions'] == 'ADMIN':
            return render_template('status/admin_login.html')
        if 'permissions' in session:
            return redirect(url_for('/'))
    return login_page()


@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/UserControler')
def UserControler():
    header = {"Content-Type": "application/json"}
    data = {}
    if 'username' in session and session['permissions']=='ADMIN':
        data['User'] = session["username"]
    else:
        return render_template('index.html')
    data = json.dumps(data)
    response = requests.post('https://asqwzx1.pythonanywhere.com/GetUsersToDelete', auth=('asqwzx1', 'NEDD'), data=data, headers=header)
    deleteUsers = eval(response.content)['data']
    response = requests.post('https://asqwzx1.pythonanywhere.com/GetUsersToReturn', auth=('asqwzx1', 'NEDD'), data=data, headers=header)
    returnUsers = eval(response.content)['data']
    return render_template('/status/admin_features/UserControl.html', UserDelete=deleteUsers, UserReturn=returnUsers)


@app.route('/DeleteUser', methods=['POST'])
def DeleteUser():
    data=dict(request.form)
    header = {"Content-Type": "application/json"}
    if 'username' in session and session['permissions']=='ADMIN':
        data['User'] = session["username"]
    else:
        return render_template('index.html')
    data = json.dumps(data)
    response = requests.post('https://asqwzx1.pythonanywhere.com/DeleteUser', auth=('asqwzx1', 'NEDD'), data=data,headers=header)
    response = eval(response.content)
    return response["status"]


@app.route('/userReturn', methods=['POST'])
def userReturn():
    data=dict(request.form)
    header = {"Content-Type": "application/json"}
    if 'username' in session and session['permissions']=='ADMIN':
        data['User'] = session["username"]
    else:
        return render_template('index.html')
    data = json.dumps(data)
    response = requests.post('https://asqwzx1.pythonanywhere.com/ReturnUser', auth=('asqwzx1', 'NEDD'), data=data,headers=header)
    response = eval(response.content)
    return response["status"]


@app.route('/AdminRequest')
def AdminRequest():
    header = {"Content-Type": "application/json"}
    data = {"User": ""}
    if 'username' in session and session['permissions'] == 'ADMIN':
        data['User'] = session["username"]
    else:
        return render_template('index.html')
    data = json.dumps(data)
    response = requests.post('https://asqwzx1.pythonanywhere.com/AdminRequest', auth=('asqwzx1', 'NEDD'), data=data, headers=header)
    response = eval(response.content)['data']
    return render_template('status/admin_features/AdminRequest.html', requests=response)


@app.route('/GetRequestJson', methods=['POST'])
def GetRequestJson():
    header = {"Content-Type": "application/json"}
    data = {"User": ""}
    if 'username' in session and session['permissions']=='ADMIN':
        data['User'] = session["username"]
    else:
        return render_template('index.html')
    data= json.dumps(data)
    response = requests.post('https://asqwzx1.pythonanywhere.com/AdminRequest', auth=('asqwzx1', 'NEDD'), data=data, headers=header)
    response = eval(response.content)
    return json.dumps(response)

@app.route('/Submit1', methods=['POST'])
def Submit1():
    data=request.form
    data=dict(data)
    header = {"Content-Type": "application/json"}
    data['insert'] = True
    if 'username' in session and session['permissions']=='ADMIN':
        data['User'] = session["username"]
    else:
        return render_template('index.html')
    data = json.dumps(data)
    response = requests.post('https://asqwzx1.pythonanywhere.com/AdminAnswers', auth=('asqwzx1', 'NEDD'), data=data,headers=header)
    response = eval(response.content)
    return response["status"]

@app.route('/Submit2', methods=['POST'])
def Submit2(data):
    data=request.form
    data=dict(data)
    header = {"Content-Type": "application/json"}
    data['insert'] = False
    if 'username' in session and session['permissions']=='ADMIN':
        data['User'] = session["username"]
    else:
        return render_template('index.html')
    data = json.dumps(data)
    response = requests.post('https://asqwzx1.pythonanywhere.com/AdminAnswers', auth=('asqwzx1', 'NEDD'), data=data,headers=header)
    response = eval(response.content)
    return response["status"]


@app.route('/login')
def login_page():
    return render_template('login.html')


def sent_to_server(data, type_request):
    data = json.dumps(data)
    header = {"Content-Type": "application/json"}
    response = requests.post('https://asqwzx1.pythonanywhere.com/'+type_request, auth=('asqwzx1', 'NEDD'),
                             data=data,
                             headers=header)
    return eval(Description.dis(str(eval(response.content)), key))

def GetPassword(user_name,password):
    conn = db_connect.connect()
    query = conn.execute("select * from Accounts WHERE username=?", (user_name,))
    result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
    if not result['data']:
        password = 'a'
    else:
        password = pbkdf2_hex(password, result['data'][0]['salt'], iterations=50000, keylen=None, hashfunc="sha256")
    return str(password)

def Sub_login(user_name, password):
    data={'pas':GetPassword(user_name,password),'user':user_name}
    response = sent_to_server(data, 'singin')
    return response


def login(user_name, password):
    response = Sub_login(user_name, password)
    if response["STATUS"] == "SUCCESS":
        session['username'] = user_name
        session['permissions'] = response['PERMISSIONS']
        return index()
    flash("there was an error please try again", category='error')
    return login_page()


def register(user, password, permissions):
    salt = password.split('$')[1]
    password = password.split('$')[2]
    data = {'User': user, 'Password': password, 'perm': permissions}
    response = sent_to_server(data, 'singup')
    if response["STATUS"] == "SUCCESS":
        try:
            conn = db_connect.connect()
            conn.execute("insert into Accounts values('{0}','{1}')".format(user, salt))
        except:
            return redirect(url_for('register_page'))
        session['username'] = user
        session['permissions'] = permissions.upper()
        return index() #TODO change to change profile
    flash("can\"t register this user", category='error')
    return register_page()


@app.route('/handle_data', methods=['POST'])
def handle_data():
    # redirect the date for the correct func
    if request.form['type_form'] == 'login':
        return login(request.form['inputIdMain'], request.form['inputPasswordMain'])
    elif request.form['type_form'] == 'register':
        return register(request.form['Register_New_User'], generate_password_hash(request.form['Register_New_Password'],
                                                                                  method='pbkdf2:sha256', salt_length=50),request.form['permissions'])
    elif request.form['type_form'] == 'admin_answer':
        return Submit2(request.form)
    elif request.form['type_form'] == 'admin_answer1':
        return Submit1(request.form)
    elif request.form['type_form'] == 'changePassword':
        return changePassword(request.form['OldPassword'], request.form['Password'])
    elif request.form['type_form'] == 'UpdateProfile':
        return UpdateProfile(request.form['Email'], request.form['tel'], request.form['address'],request.form['password'])
    return index()


@app.route('/logout')
def logout():
    # clear the session for log out
    session.clear()
    return index()

@app.route('/UpdateProfile')
def Updateprofile_page():
    return render_template('/status/normal_features/UpdateProfile.html')

def UpdateProfile(email, tel,address,password):
    response = Sub_login(session['username'], password)
    if response["STATUS"] == "SUCCESS":
        data = {'email': email, 'tel':tel, 'user':session['username'],'address':address}
        response=sent_to_server(data, "UpdateProfile")
        if response["STATUS"] == "SUCCESS":
            flash("save change", category='error')
            return index()
        else:
            flash("cant update profile", category='error')
        return Updateprofile_page()
    else:
        flash("incorect password", category='error')
    return Updateprofile_page()



@app.route('/changePassword')
def changePassword_page():
    return render_template('/status/normal_features/changePasswords.html', permission=session['permissions'])


def changePassword(oldpassword, newpassword):
    response = Sub_login(session['username'], oldpassword)
    if response["STATUS"] == "SUCCESS":
        data = {'new': GetPassword(session['username'], newpassword), 'user':session['username']}
        sent_to_server(data, "ChangePassword")
        return index()
    else:
        flash("Password Change Not Successful", category='error')
    return changePassword_page()


@app.route('/free_speaking')
def free_speaking():
    if session['username']:
        return render_template('/status/normal_features/free_speaking.html', permission=session['permissions'])
    else:
        flash("must log in", category='error')
        return index()


if __name__ == '__main__':
    app.run(debug=True)
