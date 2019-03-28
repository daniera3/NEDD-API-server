from flask import Flask, request, jsonify, Blueprint, g, redirect, render_template, session, url_for
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
import crypto2
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

db_connect = create_engine('sqlite:///nedd.db')
app = Flask(__name__)
api = Api(app)
key="NEDDNEDD"

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
            if result['data'][0]['Permissions'].upper()=="ADMIN":
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
            if result['data'][0]['Permissions'].upper()=="MANAGER":
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
            if result['data'][0]['Permissions'].upper()=="NORMAL":
                return True
            else:
                return False

class Test(Resource):
    def get(self,User,Date=datetime.datetime.now().strftime("%Y-%m-%d")):
        conn = db_connect.connect()
        query = conn.execute("select * from SpeechTasks where Date=? and User=? ",(Date,User,))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return crypto2.des(str(result),key)



    def post(Self):
	    conn = db_connect.connect()
	    User = request.json['user']
	    if 'Date' in request.json.keys():
	        Date = request.json['Date']
	    else:
	        Date=datetime.datetime.now().strftime("%Y-%m-%d")
	    query = conn.execute("select * from SpeechTasks where Date=? and User=?",(Date,User,))
	    result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
	    return crypto2.des(str(result),key)


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
            return  crypto2.des(str({'status':'Ufail'}),key)
        conn.execute("insert into SpeechTasks values('','{0}','{1}','{2}','{3}')".format(User,Line,Say,Date))
        return crypto2.des(str({'status':'success'}),key)




class Singin(Resource):
    def post(self):
        try:
            conn = db_connect.connect()
            user = request.json['user']
            pas = request.json['pas']
            query = conn.execute("select * from Accounts WHERE User=? and Active=?", (user,"True",))
            result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
            if not result['data']:
                return crypto2.des(str({'status':'Ufail'}),key)
            password=result['data'][0]['Password']
            if password==pas:
                result= {'status':'success','permissions':result['data'][0]['Permissions']}
                return crypto2.des(str(result),key)
            return  crypto2.des(str({'status':'Pfail'}),key)
        except:
            return crypto2.des(str({'status':'fail'}),key)

class singup(Resource):
    def post(self):
        conn = db_connect.connect()
        try:
            Name = request.json['User']
            Password = request.json['Password']
            Perm = request.json['perm']
            if len(Name)<=1 or len(Password)<6 or Name.count("select")!=0:
                return crypto2.des(str({'status':'hacker'}),key)
            query = conn.execute("select * from Accounts WHERE User=?", (str(Name),))
            result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
            if not result['data']:
        	    conn.execute("insert into Accounts values('{0}','{1}','{2}','{3}')".format(Name,Password,Perm,'True'))
        	    conn.execute("insert into LVL values('{0}','{1}')".format(Name,"1"))
        	    conn.execute("insert into Profile values('{0}','{1}','{2}','{3}')".format(Name,request.json['Email'],'',''))
        	    return crypto2.des(str({'status':'success'}),key)
            return crypto2.des(str({'status':'fail'}),key)
        except:
            return crypto2.des(str({'status':'fail'}),key)

class ChangePassword(Resource):
    def post(self):
        try:
            conn = db_connect.connect()
            conn.execute(" UPDATE Accounts SET Password =? WHERE User=?", (request.json['new'],str(request.json['user']),))
            return  crypto2.des(str({'status':'change password'}),key)
        except:
            return crypto2.des(str({'status':'fail ,sorry cant do this'}),key)

class AdminRequest(Resource):
    def post(self):
        conn = db_connect.connect()
        Name = request.json['User']
        if SubFunc.CheckAdmin(Name):
            query = conn.execute("select * from request")
            result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
            return crypto2.des(str(result),key)
        return crypto2.des(str({'data':[]}),key)

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
                            massge=massge+" and update"
                    except:
                        conn.execute("DELETE FROM request WHERE IDrequest = ?;",(request.json['IDrequest'],))
                        return crypto2.des(str({'status':'he can see hes info'}),key)
                conn.execute("DELETE FROM request WHERE IDrequest = ?;",(request.json['IDrequest'],))
                return  crypto2.des(str({'status':massge}),key)
            conn.execute("DELETE FROM request WHERE IDrequest = ?;",(request.json['IDrequest'],))
            return  crypto2.des(str({'status':"bad user Permissions"}),key)
        except:
            try:
                conn.execute("DELETE FROM request WHERE IDrequest = ?;",(request.json['IDrequest'],))
            except:
                return crypto2.des(str({'status':'sorry some thing happend send report bug'}),key)
            return crypto2.des(str({'status':'fail'}),key)


class SetPermissions(Resource):
    def post(self):
        conn = db_connect.connect()
        Name = request.json['User']
        if SubFunc.CheckAdmin(Name):
                Name = request.json['UserUpdate']
                query = conn.execute("select * from Accounts WHERE User=? and Active=?", (str(Name),'True',))
                result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
                if not result['data']:
                    return {'status':'fail','reason':'cannot find user'}
                if 'Permissions' in request.json.keys():
                    if request.json['Permissions']=='Admin' or request.json['Permissions']=='Manager' or request.json['Permissions']=='Normal':
                        conn.execute(" UPDATE Accounts SET Permissions =? WHERE User=?", (request.json['Permissions'],str(Name),))
                        return {'status':'sussess'}
                    else:
                        return {'status':'fail'}
                conn.execute(" UPDATE Accounts SET Permissions =? WHERE User=?", ('Normal',str(Name),))
                return {'status':'fail','reason':'return regular user'}
        return {'status':'fail','reason':'dont have Permissions'}

class GetUsersToReturn(Resource):
    def post(self):
        conn = db_connect.connect()
        try:
            Name = request.json['User']
            if SubFunc.CheckAdmin(Name):
                query = conn.execute("select User from Accounts WHERE User<>? and Active=? ORDER BY Permissions ASC;", (str(Name),"False",))
                result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
                return result
            return {'status':'haven\'t Permissions'}
        except:
            return {'status':'fail'}

class GetUsersToDelete(Resource):
    def post(self):
        conn = db_connect.connect()
        try:
            Name = request.json['User']
            if SubFunc.CheckAdmin(Name):
                query = conn.execute("select User from Accounts WHERE User<>? and Active=? ORDER BY Permissions ASC;", (str(Name),"True",))
                result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
                return result
            return {'status':'haven\'t Permissions'}
        except:
            return {'status':'fail'}




class ReturnUser(Resource):
    def post(self):
        conn = db_connect.connect()
        try:
            Name = request.json['User']
            if SubFunc.CheckAdmin(Name):
                Name = request.json['ReturnU']
                query = conn.execute("select * from Accounts WHERE User=? and Active=?", (str(Name),"False",))
                result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
                if not result['data']:
                    return {'status':'NoFind'}
                conn.execute(" UPDATE Accounts SET Active =? WHERE User=?", ('True',str(Name),))
                return {'status':'success'}
            return {'status':'fail'}
        except:
            return {'status':'fail'}

class DeleteUser(Resource):
    def post(self):
        conn = db_connect.connect()
        try:
            Name = request.json['User']
            if SubFunc.CheckAdmin(Name):
                Name = request.json['del']
                query = conn.execute("select * from Accounts WHERE User=? and Active=?", (str(Name),"True",))
                result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
                if not result['data']:
                    return {'status':'NoFind'}
                conn.execute(" UPDATE Accounts SET Active =? WHERE User=?", ('False',str(Name),))
                return {'status':'success'}
            return {'status':'fail'}
        except:
            return {'status':'fail'}

class DeleteUserTast(Resource):
    def post(self):
        conn = db_connect.connect()
        try:
            conn.execute("DELETE FROM Accounts WHERE User = ?;",(request.json['user'],))
            conn.execute("DELETE FROM LVL WHERE User = ?;",(request.json['user'],))
            return {'status':'success'}
        except:
            return {'status':'fail'}


class UpdateProfile(Resource):
    def post(self):
        try:
            conn = db_connect.connect()
            query = conn.execute("select * from Profile WHERE UserName=?", (request.json['user'],))
            result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
            if not result['data']:
                try:
                    conn.execute("insert into Profile values('{0}','{1}','{2}','{3}')".format(request.json['user'],request.json['email'],request.json['tel'],request.json['address']))
                    return crypto2.des(str({'status':'success','res':'new'}),key)
                except:
                    return crypto2.des(str({'status':'fail'}),key)
            else:
                if request.json['email']!='':
                    conn.execute(" UPDATE Profile SET email =?  WHERE UserName=?", (request.json['email'],request.json['user'],))
                if request.json['tel']!='':
                    conn.execute(" UPDATE Profile SET Tel =?  WHERE UserName=?", (request.json['tel'],request.json['user'],))
                if request.json['address']!='':
                    conn.execute(" UPDATE Profile SET address =?  WHERE UserName=?", (request.json['address'],request.json['user'],))
                return crypto2.des(str({'status':'success','res':'update'}),key)
        except:
            return crypto2.des(str({'status':'bug'}),key)


class ReturnProfile(Resource):
    def post(self):
        try:
            conn = db_connect.connect()
            Name = request.json['User']
            query = conn.execute("select * from Profile WHERE UserName=?", (str(Name),))
            result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
            if not result['data']:
                return {'status':'NoFind'}
            return crypto2.des(str(result),key)
        except:
            return {'status':'fail'}

class trylogin(Resource):
    def post(self):
        try:
            conn = db_connect.connect()
            Name = request.json['user']
            query = conn.execute("select * from Trylogin WHERE user=?", (Name,))
            result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
            date=datetime.datetime.now()
            if not result['data']:
                conn.execute("insert into Trylogin values('{0}','{1}','{2}','{3}')".format(request.json['user'],request.json['permissions'],request.json['key'],date))
                return crypto2.des(str({'status':'success','res':'new'}),key)
            else:
                conn.execute(" UPDATE Trylogin SET permissions=?,key=?,date=?  WHERE user=?", (request.json['permissions'],request.json['key'],date,Name,))
                return crypto2.des(str({'status':'success','res':'update'}),key)
        except:
            return crypto2.des(str({'status':'fail','res':'bug'}),key)


class login(Resource):
    def post(self):
        try:
            conn = db_connect.connect()
            query = conn.execute("select * from Trylogin WHERE user=? and key=? ",(request.json['user'],request.json['Key'],))
            result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
            date=datetime.datetime.now()
            if not result['data']:
                return {'status':'fail','res':'Not find'}
            else:
                try:
                    if(str(date).split(' ')[0]==result['data'][0]['date'].split(' ')[0]):
                        if(str(date).split(' ')[1].split(':')[0]==result['data'][0]['date'].split(' ')[1].split(':')[0]):
                            if((int(str(date).split(' ')[1].split(':')[1]) - int(result['data'][0]['date'].split(' ')[1].split(':')[1]))<10):
                                result['data'][0]['status']='success'
                                return result['data'][0]
                            else:
                                return {'status':'fail','res':'time over'}
                        else:
                            return {'status':'fail','res':'not some houer'}
                    else:
                        return {'status':'fail','res':'not some day'}
                except:
                    return {'status':'fail','res':'date bug'}
        except:
            return {'status':'fail','res':'bug'}


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
api.add_resource(GetUsersToReturn, '/GetUsersToReturn',methods={'POST'})
api.add_resource(GetUsersToDelete, '/GetUsersToDelete',methods={'POST'})
api.add_resource(DeleteUserTast, '/Testsingup',methods={'POST'})
api.add_resource(UpdateProfile, '/UpdateProfile',methods={'POST'})
api.add_resource(ReturnProfile, '/ReturnProfile',methods={'POST'})
api.add_resource(trylogin, '/trylogin',methods={'POST'})
api.add_resource(login, '/login',methods={'POST'})
if __name__ == '__main__':
     app.run()
