from flask import Flask, request, jsonify, Blueprint, g, redirect, render_template, session, url_for
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
import Encryption
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

db_connect = create_engine('sqlite:///nedd.db')
app = Flask(__name__)
api = Api(app)
key="NEDD"

@app.route("/")
def hello():
    return "sdsd"

class Test(Resource):
    def get(self,User,Date=datetime.datetime.now().strftime("%Y-%m-%d")):
        conn = db_connect.connect()
        query = conn.execute("select * from SpeechTasks where Date=? and User=? ",(Date,User,))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return Encryption.enc(str(result),key)



    def post(Self):
	    conn = db_connect.connect()
	    User = request.json['user']
	    if 'Date' in request.json.keys():
	        Date = request.json['Date']
	    else:
	        Date=datetime.datetime.now().strftime("%Y-%m-%d")
	    query = conn.execute("select * from SpeechTasks where Date=? and User=?",(Date,User,))
	    result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
	    return Encryption.enc(str(result),key)


class STest(Resource):
    def post(self):
        conn = db_connect.connect()
        User = request.json['user']
        Line = request.json['line']
        Say = request.json['say']
        Date = datetime.datetime.now().strftime("%Y-%m-%d")
        query = conn.execute("select * from Accounts WHERE User=? and Active='True'", (str(User),))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        if not result['data']:
            return {'status':'Ufail'}
        query = conn.execute("insert into SpeechTasks values(null,'{0}','{1}','{2}','{3}')".format(User,Line,Say,Date))
        return {'status':'success'}




class Singin(Resource):
    def get(self, user,pas):
        conn = db_connect.connect()
        query = conn.execute("select * from Accounts WHERE User=? and Active='True'", (str(user),))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        if not result['data']:
            return {'status':'Ufail'}
        if(check_password_hash(result['data'][0]['Password'],pas)):
            return {'status':'success'}
        return {'status':'Pfail'}

    def post(self):
        conn = db_connect.connect()
        user = request.json['user']
        pas = request.json['pas']
        query = conn.execute("select * from Accounts WHERE User=? and Active='True'", (str(user),))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        if not result['data']:
            return {'status':'Ufail'}
        if(check_password_hash(result['data'][0]['Password'],pas)):
            return {'status':'success'}
        return {'status':'Pfail'}

class singup(Resource):
    def post(self):
        conn = db_connect.connect()
        Name = request.json['User']
        Password = request.json['Password']
        if 'perm' in request.json.keys():
            Perm = request.json['perm']
        else:
            Perm='null'
        if len(Name)<2 or len(Password)<6 or Name.count("select")!=0:
            return {'status':'hacker'}
        query = conn.execute("select * from Accounts WHERE User=?", (str(Name),))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        if not result['data']:
        	conn.execute("insert into Accounts values('{0}','{1}','{2}',null)".format(Name,generate_password_hash(Password, method='pbkdf2:sha256', salt_length=8),Perm))
        	conn.execute("insert into LVL values('{0}',null)".format(Name))
        	return {'status':'success'}
        return {'status':'fail'}

class ChangePassword(Resource):
    def post(self):
        conn = db_connect.connect()
        Name = request.json['User']
        OldPassword = request.json['OldPassword']
        Password = request.json['Password']
        if len(Name)<2 or len(Password)<6 or len(OldPassword)<6  or Name.count("select")!=0:
            return {'status':'hacker'}
        query = conn.execute("select * from Accounts WHERE User=?", (str(Name),))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        if not result['data']:
            return {'status':'Ufail'}
        if(check_password_hash(result['data'][0]['Password'],OldPassword)):
            conn.execute(" UPDATE Accounts SET Password =? WHERE User=?", (Password,str(Name),))
            return {'status':'success'}
        return {'status':'fail'}

class SetPermissions(Resource):
    def post(self):
        conn = db_connect.connect()
        Name = request.json['User']
        query = conn.execute("select * from Accounts WHERE User=?", (str(Name),))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        if not result['data']:
            return {'status':'fail'}
        else:
            if result['data'][0]['Permissions']=="Admin":
                Name = request.json['UserUpdate']
                query = conn.execute("select * from Accounts WHERE User=? and Active=?", (str(Name),'True',))
                result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
                if not result['data']:
                    return {'status':'NoFind'}
                if 'Permissions' in request.json.keys():
                    if request.json['Permissions']=='Admin' or request.json['Permissions']=='Manager' or request.json['Permissions']=='Nurmal':
                        conn.execute(" UPDATE Accounts SET Permissions =? WHERE User=?", (request.json['Permissions'],str(Name),))
                    else:
                        return {'status':'fail'}
                conn.execute(" UPDATE Accounts SET Permissions =? WHERE User=?", ('Nurmal',str(Name),))
                return {'status':'success'}
        return {'status':'fail'}

class ReturnUser(Resource):
    def post(self):
        conn = db_connect.connect()
        Name = request.json['User']
        query = conn.execute("select * from Accounts WHERE User=?", (str(Name),))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        if not result['data']:
            return {'status':'fail'}
        else:
            if result['data'][0]['Permissions']=='Admin':
                Name = request.json['ReturnU']
                query = conn.execute("select * from Accounts WHERE User=? and Active=?", (str(Name),"False",))
                result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
                if not result['data']:
                    return {'status':'NoFind'}
                conn.execute(" UPDATE Accounts SET Active =? WHERE User=?", ('True',str(Name),))
                return {'status':'success'}
        return {'status':'fail'}

class DeleteUser(Resource):
    def post(self):
        conn = db_connect.connect()
        Name = request.json['User']
        query = conn.execute("select * from Accounts WHERE User=?", (str(Name),))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        if not result['data']:
            return {'status':'fail'}
        else:
            if result['data'][0]['Permissions']=='Admin':
                Name = request.json['del']
                query = conn.execute("select * from Accounts WHERE User=? and Active=?", (str(Name),"True",))
                result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
                if not result['data']:
                    return {'status':'NoFind'}
                conn.execute(" UPDATE Accounts SET Active =? WHERE User=?", ('False',str(Name),))
                return {'status':'success'}
        return {'status':'fail'}


api.add_resource(Singin,  '/singin','/singin/<user>/<pas>',methods={'POST','GET'})
api.add_resource(Test, '/test','/test/<User>/<Date>','/test/<User>',methods={'POST','GET'})
api.add_resource(STest, '/stest',methods={'POST'})
api.add_resource(singup, '/singup',methods={'POST'})
api.add_resource(DeleteUser, '/DeleteUser',methods={'POST'})
api.add_resource(ReturnUser, '/ReturnUser',methods={'POST'})
api.add_resource(SetPermissions, '/SetPermissions',methods={'POST'})
api.add_resource(ChangePassword, '/ChangePassword',methods={'POST'})
if __name__ == '__main__':
     app.run()
