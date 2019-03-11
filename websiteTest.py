from flask import *
import requests
from json import *
from os import urandom
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
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


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/handle_data', methods=['POST'])
def handle_data():
    user=request.form['username']
    password=request.form['password']
    header={ "Content-Type": "application/json"}
    data = {"user":"", "pas":""}
    data['user']=user
    data['pas']=password
    data=json.dumps(data)
    response = requests.post('https://asqwzx1.pythonanywhere.com/singin', auth=('asqwzx1', 'NEDD'), data=data, headers=header)
    if eval(response.content)["status"]=="success":
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return redirect(url_for('login'))


@app.route('/Register_data', methods=['POST'])
def Register_data():

    user=request.form['username']
    password=generate_password_hash(request.form['password'], method='pbkdf2:sha256', salt_length=8)
    header={ "Content-Type": "application/json"}
    data = {"User":"","Password":""}
    data['User']=user
    data['Password']=password
    data=json.dumps(data)
    response = requests.post('https://asqwzx1.pythonanywhere.com/singup', auth=('asqwzx1', 'NEDD'),data=data, headers=header)
    if eval(response.content)["status"]=="success":
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return redirect(url_for('register'))




@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('response', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
     app.run(debug=True)





