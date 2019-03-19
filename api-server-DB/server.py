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

@app.route('/')
def index():
    return "hi"


class SubFunc():
    def CheckAdmin(user):
        conn = db_connect.connect()
        query = conn.execute("select * from Accounts WHERE User=? and Active=?""", (str(user),"True",))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        if not result['data']:
            return False
        else:
            if result['data'][0]['Permissions']=="Admin":
                return True
            else:
                return False

    def CheckManager(user):
        conn = db_connect.connect()
        query = conn.execute("select * from Accounts WHERE User=? and Active=?""", (str(user),"True",))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        if not result['data']:
            return False
        else:
            if result['data'][0]['Permissions']=="Manager":
                return True
            else:
                return False

    def CheckNormal(user):
        conn = db_connect.connect()
        query = conn.execute("select * from Accounts WHERE User=? and Active=?""", (str(user),"True",))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        if not result['data']:
            return False
        else:
            if result['data'][0]['Permissions']=="Normal":
                return True
            else:
                return False


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
        query = conn.execute("select * from Accounts WHERE User=? and Active=?", (User,"True",))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        if not result['data']:
            return {'status':'Ufail'}
        conn.execute("insert into SpeechTasks values('','{0}','{1}','{2}','{3}')".format(User,Line,Say,Date))
        return {'status':'success'}




class Singin(Resource):
    def post(self):
        conn = db_connect.connect()
        user = request.json['user']
        pas = request.json['pas']
        query = conn.execute("select * from Accounts WHERE User=? and Active=?", (user,"True",))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        if not result['data']:
            return Encryption.enc(str({'status':'Ufail'}),key)
        if check_password_hash(result['data'][0]['Password'],pas):
            result= {'status':'success','Permissions':result['data'][0]['Permissions']}
            return Encryption.enc(str(result),key)
        return  Encryption.enc(str({'status':'Pfail'}),key)

class singup(Resource):
    def post(self):
        conn = db_connect.connect()
        Name = request.json['User']
        Password = request.json['Password']
        Perm = request.json['perm']
        if len(Name)<=1 or len(Password)<6 or Name.count("select")!=0:
            return {'status':'hacker'}
        query = conn.execute("select * from Accounts WHERE User=?", (str(Name),))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        if not result['data']:
        	conn.execute("insert into Accounts values('{0}','{1}','{2}','{3}')".format(Name,Password,Perm,'True'))
        	conn.execute("insert into LVL values('{0}','{1}')".format(Name,"1"))
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

class AdminRequest(Resource):
    def post(self):
        conn = db_connect.connect()
        Name = request.json['User']
        if SubFunc.CheckAdmin(Name):
            query = conn.execute("select * from request")
            result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
            return result
        return {'data':[]}

class AdminAnswersToRequests(Resource):
    def post(self):
        massge="deleted this request"
        conn = db_connect.connect()
        try:
            Name = request.json['User']
            if SubFunc.CheckAdmin(Name) and SubFunc.CheckManager(request.json['requesting']) and SubFunc.CheckNormal(request.json['user']) :
                if request.json['insert']:
                    try:
                        query = conn.execute("select * from Guider where User=? AND GuideName=?",(request.json['user'],request.json['requesting'],))
                        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
                        if not result['data']:
                            conn.execute("insert into Guider values('{0}','{1}','True')".format(request.json['user'],request.json['requesting']))
                            massge=massge+" and saved"
                        else:
                            conn.execute(" UPDATE Guider SET Active =? where User=? AND GuideName=?",("True",request.json['user'],request.json['requesting'],))
                            massge=massge+" and updata"
                    except:
                        conn.execute("DELETE FROM request WHERE IDrequest = ?;",(request.json['IDrequest'],))
                        return {'status':'he can see hes info'}
                conn.execute("DELETE FROM request WHERE IDrequest = ?;",(request.json['IDrequest'],))
                return {'status':massge}
            conn.execute("DELETE FROM request WHERE IDrequest = ?;",(request.json['IDrequest'],))
            return {'status':"bad user Permissions"}
        except:
            return {'status':'fail'}


class SetPermissions(Resource):
    def post(self):
        conn = db_connect.connect()
        Name = request.json['User']
        if SubFunc.CheckAdmin(Name):
                Name = request.json['UserUpdate']
                query = conn.execute("select * from Accounts WHERE User=? and Active=?", (str(Name),'True',))
                result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
                if not result['data']:
                    return {'status':'NoFind'}
                if 'Permissions' in request.json.keys():
                    if request.json['Permissions']=='Admin' or request.json['Permissions']=='Manager' or request.json['Permissions']=='Normal':
                        conn.execute(" UPDATE Accounts SET Permissions =? WHERE User=?", (request.json['Permissions'],str(Name),))
                    else:
                        return {'status':'fail'}
                conn.execute(" UPDATE Accounts SET Permissions =? WHERE User=?", ('Normal',str(Name),))
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
api.add_resource(AdminRequest, '/AdminRequest',methods={'POST'})
api.add_resource(AdminAnswersToRequests, '/AdminAnswers',methods={'POST'})

if __name__ == '__main__':
     app.run()
