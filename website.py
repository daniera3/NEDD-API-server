from flask import Flask, render_template, request, session, url_for, redirect, json, flash,jsonify
import requests
from os import urandom
from werkzeug.security import generate_password_hash,pbkdf2_hex
import Description

from sqlalchemy import create_engine


app = Flask(__name__)
key="NEDD"
#db in site for salt
db_connect = create_engine('sqlite:///nedd.db')

app.secret_key = urandom(16)

my_domain = 'asqwzx1.pythonanywhere.com/'
username = 'asqwzx1'
token = '973c7adaa1a72b549a6120af137ba68137ec2351'


@app.route('/')
def index():
    if session.get('username'):
        if session['permissions'] == 'NORMAL':
            return render_template('status/normal_login.html')
        if session['permissions'] == 'MANGER':
            return render_template('status/parent_login.html')
        if session['permissions'] == 'ADMIN':
            return render_template('status/admin_login.html')
    return render_template('login.html')


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
    return render_template('/status/admin_features/UserControl.html', UserDelete=deleteUsers,UserReturn=returnUsers)


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
    if 'username' in session and session['permissions']=='ADMIN':
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
def Submit2():
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


def login(user_name, password):
    data = {"user": user_name}
    conn = db_connect.connect()
    query = conn.execute("select * from Accounts WHERE username=?", (user_name,))
    result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
    if not result['data']:
        password ='a'
    else:
        password= pbkdf2_hex(password, result['data'][0]['salt'], iterations=50000, keylen=None, hashfunc="sha256")
    data['pas'] = str(password)
    response = sent_to_server(data, 'singin')
    if response["STATUS"] == "SUCCESS":
        session['username'] = user_name
        session['permissions'] = response['PERMISSIONS']
        return index()
    message = "there was an error please try again"
    flash(message, category='erorr')
    return redirect(url_for('login_page'))


def register(user,password,permissions):
    salt=password.split('$')[1]
    data = {}
    data['User'] = user
    data['Password'] = password
    data['perm'] = permissions
    response = sent_to_server(data, 'singup')
    if response["STATUS"] == "SUCCESS":
        try:
            conn = db_connect.connect()
            conn.execute("insert into Accounts values('{0}','{1}')".format(user, salt))
        except:
            return redirect(url_for('register_page'))
        session['username'] = user
        session['permissions']=permissions.upper()
        return index()
    flash("cant register this user", category='erorr')
    return redirect(url_for('register_page'))


@app.route('/handle_data', methods=['POST'])
def handle_data():
    if request.form['type_form'] == 'login':
        return login(request.form['inputIdMain'], request.form['inputPasswordMain'])
    elif request.form['type_form'] == 'register':
        return register(request.form['Register_New_User'], generate_password_hash(request.form['Register_New_Password'], method='pbkdf2:sha256', salt_length=50), request.form['permissions'])
    return index()


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('response', None)
    session.pop('permissions', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)