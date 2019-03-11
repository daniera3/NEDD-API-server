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
    session['username'] = request.form['username']
    header={ "Content-Type": "application/json"}
    #data = {"user":request.form['username'],"pas":generate_password_hash(request.form['password'], method='pbkdf2:sha256', salt_length=8)}
    data = '{"user":"sdsd", "pas":"sadasd"}'
    response = requests.post('https://asqwzx1.pythonanywhere.com/singin', data=data, headers=header)

    session['response']=response.content

    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('response', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
     app.run(debug=true)





