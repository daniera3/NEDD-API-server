# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, request, session, url_for, redirect, json, flash
import requests
from os import urandom
from json import dumps
from werkzeug.security import  generate_password_hash
import Description


app = Flask(__name__)
key="NEDD"




app.secret_key = urandom(16)

my_domain = 'asqwzx1.pythonanywhere.com/'
username = 'asqwzx1'
token = '973c7adaa1a72b549a6120af137ba68137ec2351'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register')
def register():
    return render_template('register.html')




@app.route('/AdminRequest')
def AdminRequest():
    header = {"Content-Type": "application/json"}
    data = {"User": ""}
    data['User'] = session["username"]
    data = json.dumps(data)
    response = requests.post('https://asqwzx1.pythonanywhere.com/AdminRequest', auth=('asqwzx1', 'NEDD'), data=data, headers=header)
    response = eval(response.content)['data']
    return render_template('AdminRequest.html', requests=response)

@app.route('/Submit1', methods=['POST'])
def Submit1():
    data=request.form
    data=dict(data)
    header = {"Content-Type": "application/json"}
    data['insert'] = True
    data['User'] = session["username"]
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
    data['User'] = session["username"]
    data = json.dumps(data)
    response = requests.post('https://asqwzx1.pythonanywhere.com/AdminAnswers', auth=('asqwzx1', 'NEDD'), data=data,headers=header)
    response = eval(response.content)
    return response["status"]



@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/handle_data', methods=['POST'])
def handle_data():
    user=request.form['inputIdMain']
    password=request.form['inputPasswordMain']
    header={ "Content-Type": "application/json"}
    data = {"user":"", "pas":""}
    data['user']=user
    data['pas']=password
    data=json.dumps(data)
    response = requests.post('https://asqwzx1.pythonanywhere.com/singin', auth=('asqwzx1', 'NEDD'), data=data, headers=header)
    response=eval(Description.dis(str(eval(response.content)),key))
    if response["STATUS"]=="SUCCESS":
        session['username'] = request.form['inputIdMain']
        session['permissions']=response['PERMISSIONS']
        login_user(response['PERMISSIONS'])
        return redirect(url_for('index'))
    message="NEED WIRTE SOMTHING HER FOR ERORR"
    flash(message, category='erorr')
    return redirect(url_for('login'))


@app.route('/Register_data', methods=['POST'])
def Register_data():
    user = request.form['Register_New_User']
    permissions = request.form['permissions']
    password = generate_password_hash(request.form['Register_New_Password'], method='pbkdf2:sha256', salt_length=8)
    header = { "Content-Type": "application/json"}
    data = {"User":"","Password":"","perm":""}
    data['User'] = user
    data['Password'] = password
    data['perm'] = permissions
    data = json.dumps(data)
    response = requests.post('https://asqwzx1.pythonanywhere.com/singup', auth=('asqwzx1', 'NEDD'), data=data, headers=header)
    if eval(response.content)["status"] == "success":
        session['username'] = request.form['Register_New_User']
        session['permissions']=permissions.upper()
        return redirect(url_for('index'))
    message="NEED WIRTE SOMTHING HER FOR ERORR"
    flash(message, category='erorr')
    return redirect(url_for('register'))




@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('response', None)
    session.pop('permissions', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()