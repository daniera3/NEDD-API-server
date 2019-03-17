from flask import Flask, render_template, request, session, url_for, redirect, json, flash,jsonify
import requests
from os import urandom
from werkzeug.security import generate_password_hash
import Description


app = Flask(__name__)
key = "NEDD"


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




@app.route('/AdminRequest')
def AdminRequest():
    header = {"Content-Type": "application/json"}
    data = {"User": ""}
    data['User'] = session["username"]
    data = json.dumps(data)
    response = requests.post('https://asqwzx1.pythonanywhere.com/AdminRequest', auth=('asqwzx1', 'NEDD'), data=data, headers=header)
    response = eval(response.content)['data']
    return render_template('status/admin_features/AdminRequest.html', requests=response)


@app.route('/GetRequestJson', methods=['POST'])
def GetRequestJson():
    header = {"Content-Type": "application/json"}
    data = {"User": ""}
    data['User'] = session["username"]
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
    data['User'] = session["username"]
    data = json.dumps(data)
    flash(data, category='erorr')
    response = requests.post('https://asqwzx1.pythonanywhere.com/AdminAnswers', auth=('asqwzx1', 'NEDD'), data=data,headers=header)
    response = eval(response.content)
    return response["status"]

@app.route('/Submit2', methods=['POST'])
def Submit2():
    data=request.form
    data=dict(data)
    header = {"Content-Type": "application/json"}
    data['insert'] = False
    data['User'] = session["username"]
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
    data = {"user": user_name, "pas": password}
    response = sent_to_server(data, 'singin')
    session['eror']=response
    if response["STATUS"] == "success":
        session['username'] = user_name
        session['permissions'] = response['PERMISSIONS']
        return index()
    message = "there was an error please try again"
    flash(message, category='erorr')
    return redirect(url_for('login_page'))


#TODO fix the registrate function
    #need to add encryption to server side
def register(user_name, password, type_user):
    password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
    data = {"User": user_name, "Password": password, "perm": type_user}
    response = sent_to_server(data, 'singup')
    session['eror'] = response
    if response["STATUS"] == "success":
        session['username'] = request.form['Register_New_User']
        session['permissions'] = type_user.upper()
        return redirect(url_for('index'))
    message = "there was an error please try again"
    flash(message, category='erorr')
    return redirect(url_for('register_page'))


@app.route('/handle_data', methods=['POST'])
def handle_data():
    if request.form['type_form'] == 'login':
        return login(request.form['inputIdMain'], request.form['inputPasswordMain'])
    elif request.form['type_form'] == 'register':
        return register(request.form['Register_New_User'], request.form['Register_New_Password'], request.form['permissions'])
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