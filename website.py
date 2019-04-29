#!/usr/bin/env python3
from flask import Flask, render_template, request, session, url_for, redirect, json, flash
import requests
from os import urandom
from werkzeug.security import generate_password_hash, pbkdf2_hex
import crypto2
from sqlalchemy import create_engine
from flask_mail import Mail, Message
import random

app = Flask(__name__)

key = "NEDDNEDD"


#db in site for salt
db_connect = create_engine('sqlite:///nedd.db')

my_domain = 'asqwzx1.pythonanywhere.com/'
username = 'asqwzx1'
token = '973c7adaa1a72b549a6120af137ba68137ec2351'

app = Flask(__name__)


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'neddproject@gmail.com'
app.config['MAIL_PASSWORD'] = 'nedd123456'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

app.secret_key = urandom(16)


def sendmail(header, email, massge):
    try:
        msg = Message(header, sender = 'neddproject@gmail.com', recipients = [email])
        msg.body = massge
        mail.send(msg)
        return "send"
    except:
        return "fail"


@app.route('/')
def index():
    if 'permissions' in session:
        if session['permissions'] == 'NORMAL':
            return render_template('status/normal_login.html')
        if session['permissions'] == 'MANGER':
            return render_template('status/parent_login.html')
        if session['permissions'] == 'ADMIN':
            return render_template('status/admin_login.html')
    return login_page()


@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/UserControler')
def UserControler():
    data = {}
    if 'username' in session and session['permissions']=='ADMIN':
        data['User'] = session["username"]
    else:
        return render_template('index.html')
    response=sent_to_server(json.dumps(data),"GetUsersToReturn")
    returnUsers = (response)['data']

    data['Permissions']='Admin'
    response = sent_to_server(json.dumps(data), "GetUsersPerPermissions")
    admins = (response)['data']

    data['Permissions'] = 'Manger'
    response = sent_to_server(json.dumps(data), "GetUsersPerPermissions")
    Mangers = (response)['data']

    data['Permissions'] = 'Normal'
    response = sent_to_server(json.dumps(data), "GetUsersPerPermissions")
    Normals = (response)['data']
    deleteUsers=admins+Mangers+Normals
    return render_template('/status/admin_features/UserControl.html', UserDelete=deleteUsers, UserReturn=returnUsers,UserAdmin=admins,UserManger=Mangers,UserNormal=Normals,AllUsers=deleteUsers+returnUsers)



@app.route('/AddWord')
def Add_word_page():
    data = {}
    if 'username' in session and (session['permissions'] == 'ADMIN' or session['permissions'] == 'MANGER'):
        data['User'] = session["username"]
    else:
        return render_template('index.html')
    response = sent_to_server(json.dumps(data), "trainee")
    trainee = (response)['data']
    return render_template('/status/manger_features/addWords.html', trainee=trainee)


@app.route('/DeleteUser', methods=['POST'])
def DeleteUser():
    data=dict(request.form)
    if 'username' in session and session['permissions']=='ADMIN':
        data['User'] = session["username"]
    else:
        return render_template('index.html')
    data = json.dumps(data)
    response=sent_to_server(data, "DeleteUser")
    return response["status"]


@app.route('/userReturn', methods=['POST'])
def userReturn():
    data=dict(request.form)
    if 'username' in session and session['permissions']=='ADMIN':
        data['User'] = session["username"]
    else:
        return render_template('index.html')
    data = json.dumps(data)
    response=sent_to_server(data,"ReturnUser")
    return response["status"]

@app.route('/SetPermissions', methods=['POST'])
def SetPermissions(data,url):
    if 'username' in session and session['permissions']=='ADMIN':
        data['User'] = session["username"]
    else:
        return render_template('index.html')
    data = json.dumps(data)
    response=sent_to_server(data,url)
    return response["status"]


@app.route('/AdminRequest')
def AdminRequest():
    data = {"User": ""}
    if 'username' in session and session['permissions'] == 'ADMIN':
        data['User'] = session["username"]
    else:
        return render_template('index.html')
    data = json.dumps(data)
    response=sent_to_server(data,"AdminRequest")
    response = (response)['data']
    return render_template('status/admin_features/AdminRequest.html', requests=response)


@app.route('/GetRequestJson', methods=['POST'])
def GetRequestJson():
    data = {"User": ""}
    if 'username' in session and session['permissions']=='ADMIN':
        data['User'] = session["username"]
    else:
        return render_template('index.html')
    data= json.dumps(data)
    response=sent_to_server(data,"AdminRequest")
    return json.dumps(response)

@app.route('/Submit1', methods=['POST'])
def Submit1():
    data = request.form
    data = dict(data)
    data['insert'] = True
    if 'username' in session and session['permissions'] == 'ADMIN':
        data['User'] = session["username"]
    else:
        return render_template('index.html')
    response=sent_to_server(data,"AdminAnswers")
    return response["status"]

@app.route('/Submit2', methods=['POST'])
def Submit2():
    data = request.form
    data = dict(data)
    data['insert'] = False
    if 'username' in session and session['permissions'] == 'ADMIN':
        data['User'] = session["username"]
    else:
        return render_template('index.html')
    response = sent_to_server(data, "AdminAnswers")
    return response["status"]


@app.route('/login')
def login_page():
    return render_template('login.html')


def sent_to_server(data, type_request):
    temp = {"data": crypto2.des(str(data), key)}
    data = json.dumps(temp)
    header = {"Content-Type": "application/json"}
    response = requests.post('https://asqwzx1.pythonanywhere.com/'+type_request, auth=('asqwzx1', 'NEDD'),
                             data=data,
                             headers=header)
    return eval(crypto2.des_dicrypte(str(eval(response.content)), key))


def GetPassword(user_name, password):
    conn = db_connect.connect()
    query = conn.execute("select * from Accounts WHERE username=?", (user_name,))
    result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
    if not result['data']:
        password = 'a'
    else:
        password = pbkdf2_hex(password, result['data'][0]['salt'], iterations=150000, keylen=None, hashfunc="sha256")
    return str(password)


def Sub_login(user_name, password):
    data={'pas':GetPassword(user_name,password),'user':user_name}
    response = sent_to_server(data, 'singin')
    return response


def login(user_name, password):
    response = Sub_login(user_name, password)
    if response['status'] == "success":
        if user_name=='admin':
            session['username'] = user_name
            session['permissions'] = response['permissions'].upper()
            return index()
        return enterkey(user_name,response['permissions'])
    flash("there was an error please try again", category='error')
    return login_page()


def getprofile(user):

    data = {'User': user}
    response = sent_to_server(data, 'ReturnProfile')
    if 'status' in response:
        return {'email': '', 'Tel': '', 'address': ''}
    return json.dumps(response['data'][0])


def enterkey(user,permissions):
    Key=random.randint(10000000,100000000)
    email=eval(getprofile(user))
    email=email['email']
    header='login key'
    massge="you key for login to NEDD site is:'{0}'".format(Key)
    status=sendmail(header,str(email),massge)
    data={'user':user,'permissions':permissions,'key':Key}
    sent_to_server(data, 'trylogin')
    if status=='fail':
        return login_page()
    return render_template('login_key.html',User=user)




def register(user, password, permissions,Email):
    salt = password.split('$')[1]
    password = password.split('$')[2]
    data = {'User': user, 'Password': password, 'perm': permissions,'Email':Email}
    response = sent_to_server(data, 'singup')
    if response["status"] == "success":
        try:
            conn = db_connect.connect()
            conn.execute("insert into Accounts values('{0}','{1}')".format(user, salt))
        except:
            data = {'user': user}
            sent_to_server(data, "Testsingup")
            return redirect(url_for('register_page'))
        session['username'] = user
        session['permissions'] = permissions.upper()
        return index()
    flash("can\"t register this user", category='error')
    return register_page()


@app.route('/handle_data', methods=['POST'])
def handle_data():
    # redirect the date for the correct func
    if request.form['type_form'] == 'login':
        return login(request.form['inputIdMain'], request.form['inputPasswordMain'])
    elif request.form['type_form'] == 'register':
        return register(request.form['Register_New_User'], generate_password_hash(request.form['Register_New_Password'],method='pbkdf2:sha256', salt_length=50),request.form['permissions'],request.form['Email'])
    elif request.form['type_form'] == 'admin_answer':
        return Submit2(request.form)
    elif request.form['type_form'] == 'admin_answer1':
        return Submit1(request.form)
    elif request.form['type_form'] == 'Endlogin':
        return Endlogin(request.form['user'],request.form['key'])
    elif request.form['type_form'] == 'changePassword':
        return changePassword(request.form['OldPassword'], request.form['Password'])
    elif request.form['type_form'] == 'UpdateProfile':
        return UpdateProfile(request.form['Email'], request.form['tel'], request.form['address'],request.form['password'])
    elif request.form['type_form'] == 'RequestPermissions':
        return RequestPermissions(dict(request.form))
    elif request.form['type_form'] == 'SetPermissions':
        return SetPermissions(dict(request.form), "SetPermissions")
    elif request.form['type_form'] == 'getUserData':
        return getprofile(request.form['user'])
    elif request.form['type_form'] == 'SaveTest':
        return SaveTest(dict(request.form))
    elif request.form['type_form'] == 'addwords':
        return AddWord(dict(request.form))
    return index()

def AddWord(data):
    if 'username' in session:
        data['User'] = session['username']
    answer = sent_to_server(json.dumps(data), "addword")
    return answer['status']

def SaveTest(data):
    if 'username' in session:
        data['user'] = session['username']
    answer = sent_to_server(json.dumps(data), "stest")
    return answer['status']

def RequestPermissions(data):
    if 'username' in session:
        data['user']=session['username']
        answer = sent_to_server(json.dumps(data), "RequestPermissions")
        flash(answer['status'])
        return RequestPermissions_page()
    else:
        return index()


def Endlogin(user,Key):
    data={'user':user,'Key':Key}
    response=sent_to_server(data,'login')
    if response["status"] == "success" or Key=='' :
        session['username']=user
        session['permissions']=response['permissions'].upper()
        return index()
    else:
        flash("bad key", category='error')
        return render_template('login_key.html', User=user)



@app.route('/logout')
def logout():
    # clear the session for log out
    session.clear()
    return index()

@app.route('/UpdateProfile')
def Updateprofile_page():
    if 'username' not in session:
        return login_page()
    return render_template('/status/normal_features/UpdateProfile.html')

@app.route('/Showprofile')
def Showprofile_page():
    if 'username' in session:
        profile=eval(getprofile(session['username']))
        email=profile['email']
        Tel = profile['Tel']
        address = profile['address']

    else:
        return index()
    return render_template('/status/normal_features/ShowProfile.html', email=email,Tel=Tel,address=address)


def UpdateProfile(email, tel,address,password):
    if 'username' not in session:
        return login_page()
    response = Sub_login(session['username'], password)
    if response["status"] == "success":
        data = {'email': email, 'tel':tel, 'user':session['username'],'address':address}
        response=sent_to_server(data, "UpdateProfile")
        if response["status"] == "success":
            flash("save change", category='error')
            return index()
        else:
            flash("cant update profile", category='error')
        return Updateprofile_page()
    else:
        flash("incorect password", category='error')
    return Updateprofile_page()


@app.route('/RequestPermissions')
def RequestPermissions_page():
    if 'username' not in session:
        return login_page()
    return render_template('/status/manger_features/requset_pramission.html')


@app.route('/changePassword')
def changePassword_page():
    if 'username' not in session:
        return login_page()
    return render_template('/status/normal_features/changePasswords.html', permission=session['permissions'])


def changePassword(oldpassword, newpassword):
    if 'username' not in session:
        return login_page()
    response = Sub_login(session['username'], oldpassword)
    if response["status"] == "success":
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

@app.route('/speech_game')
def speech_game():
    if 'username' in session:
        return render_template('/status/normal_features/speech_game.html', permission=session['permissions'])
    else:
        flash("must log in", category='error')
        return index()

@app.route('/get_student_result')
def get_student_result():
    if 'username' in session:
        return render_template('/status/manger_features/student_statistics.html', permission=session['permissions'])
    else:
        flash("must log in", category='error')
        return index()


if __name__ == '__main__':
    app.run(debug=True)
