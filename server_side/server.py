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

    def CheckManger(user):
        conn = db_connect.connect()
        query = conn.execute("select * from Accounts WHERE User=? and Active=?""", (str(user),"True",))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        if not result['data']:
            return False
        else:
            if result['data'][0]['Permissions'].upper()=="MANGER":
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
	    DATA=eval(crypto2.des_dicrypte((request.json['data']), key))
	    User = DATA['user']
	    if 'Date' in DATA.keys():
	        Date = DATA['Date']
	    else:
	        Date=datetime.datetime.now().strftime("%Y-%m-%d")
	    query = conn.execute("select * from SpeechTasks where Date=? and User=?",(Date,User,))
	    result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
	    return crypto2.des(str(result),key)


class STest(Resource):
    def post(self):
        try:
            DATA=eval(crypto2.des_dicrypte(request.json['data'], key))
            conn = db_connect.connect()
            User = DATA['user']
            query = conn.execute("select * from Accounts WHERE User=? and Active=?", (User,"True",))
            result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
            if not result['data']:
                return  crypto2.des(str({'status':'fail'}),key)
            Date = datetime.datetime.now().strftime("%Y-%m-%d")
            line=DATA['line']
            say=DATA['say']
            grade=DATA['grade']
            try:
                conn.execute("insert into SpeechTasks values(NULL,'{0}','{1}','{2}','{3}','{4}')".format(User,line,say,grade,Date))
            except:
                return crypto2.des(str({'status':'bug save'}),key)

            return crypto2.des(str({'status':'save'}),key)
        except:
            return crypto2.des(str({'status':'bug'}),key)



class Singin(Resource):
    def post(self):
        DATA=eval(crypto2.des_dicrypte(request.json['data'], key))
        try:
            conn = db_connect.connect()
            user = DATA['user']
            pas = DATA['pas']
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
        DATA=eval(crypto2.des_dicrypte((request.json['data']), key))
        conn = db_connect.connect()
        try:
            Name = DATA['User']
            Password = DATA['Password']
            Perm = DATA['perm']

            if len(Name)<=1 or len(Password)<6 or Name.count("select")!=0 or Perm not in ["normal","Normal","mannger","Manger"]:
                return crypto2.des(str({'status':'hacker'}),key)
            print(Perm)
            query = conn.execute("select * from Accounts WHERE User=={0}".format(Name))
            print("got har:")
            result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
            if not result['data']:
        	    conn.execute("insert into Accounts values('{0}','{1}','{2}','{3}')".format(Name,Password,Perm,'True'))
        	    conn.execute("insert into LVL values('{0}','{1}')".format(Name,"1"))
        	    conn.execute("insert into Profile values('{0}','{1}','{2}','{3}')".format(Name,DATA['Email'],'',''))
        	    return crypto2.des(str({'status':'success'}),key)
            return crypto2.des(str({'status':'fail'}),key)
        except:
            try:
                conn.execute("DELETE FROM Accounts WHERE User = ?;",(DATA['user'],))
                conn.execute("DELETE FROM LVL WHERE User = ?;",(DATA['user'],))
                conn.execute("DELETE FROM Profile WHERE UserName = ?;",(DATA['user'],))
                return crypto2.des(str({'status':'failAndDeleted'}),key)
            except:
                return crypto2.des(str({'status':'failAndCrash'}),key)

class ChangePassword(Resource):
    def post(self):
        DATA=eval(crypto2.des_dicrypte((request.json['data']), key))
        try:
            conn = db_connect.connect()
            conn.execute(" UPDATE Accounts SET Password =? WHERE User=?", (DATA['new'],str(DATA['user']),))
            return  crypto2.des(str({'status':'change password'}),key)
        except:
            return crypto2.des(str({'status':'fail ,sorry cant do this'}),key)

class AdminRequest(Resource):
    def post(self):
        DATA=eval(crypto2.des_dicrypte((request.json['data']), key))
        conn = db_connect.connect()
        Name = DATA['User']
        if SubFunc.CheckAdmin(Name):
            query = conn.execute("select * from request")
            result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
            return crypto2.des(str(result),key)
        return crypto2.des(str({'data':[]}),key)

class AdminAnswersToRequests(Resource):
    def post(self):
        DATA=eval(crypto2.des_dicrypte((request.json['data']), key))
        massge="deleted this request"
        conn = db_connect.connect()
        try:
            Name = DATA['User']
            if SubFunc.CheckAdmin(Name) and (SubFunc.CheckManger(DATA['requesting'])or SubFunc.CheckAdmin(DATA['requesting']))and SubFunc.CheckNormal(DATA['user']) :
                if DATA['insert']:
                    try:
                        query = conn.execute("select * from Guider where User=? AND GuideName=?",(DATA['user'],DATA['requesting'],))
                        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
                        if not result['data']:
                            conn.execute("insert into Guider values('{0}','{1}','True')".format(DATA['user'],DATA['requesting']))
                            massge=massge+" and saved"
                        else:
                            conn.execute(" UPDATE Guider SET Active =? where User=? AND GuideName=?",("True",DATA['user'],DATA['requesting'],))
                            massge=massge+" and update"
                        conn.execute("DELETE FROM request WHERE requesting = ? and user=?;",(DATA['requesting'],DATA['user'],))
                    except:
                        conn.execute("DELETE FROM request WHERE IDrequest = ?;",(DATA['IDrequest'],))
                        return crypto2.des(str({'status':'he can see hes info'}),key)
                conn.execute("DELETE FROM request WHERE IDrequest = ?;",(DATA['IDrequest'],))
                return  crypto2.des(str({'status':massge}),key)
            conn.execute("DELETE FROM request WHERE IDrequest = ?;",(DATA['IDrequest'],))
            return  crypto2.des(str({'status':"bad user Permissions"}),key)
        except:
            try:
                conn.execute("DELETE FROM request WHERE IDrequest = ?;",(DATA['IDrequest'],))
            except:
                return crypto2.des(str({'status':'sorry some thing happend send report bug'}),key)
            return crypto2.des(str({'status':'fail'}),key)


class SetPermissions(Resource):
    def post(self):

        DATA=eval(crypto2.des_dicrypte((request.json['data']), key))
        conn = db_connect.connect()
        Name = DATA['User']
        if SubFunc.CheckAdmin(Name):
                Name = DATA['UserUpdate']
                query = conn.execute("select * from Accounts WHERE User=? and Active=?", (str(Name),'True',))
                result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
                if not result['data']:
                    return crypto2.des(str({'status':'fail','reason':'cannot find user'}),key)
                if 'Permissions' in DATA.keys():
                    if DATA['Permissions']=='Admin' or DATA['Permissions']=='Manger' or DATA['Permissions']=='Normal':
                        conn.execute(" UPDATE Accounts SET Permissions =? WHERE User=?", (DATA['Permissions'],str(Name),))
                        return crypto2.des(str({'status':'success'}),key)
                    else:
                        return crypto2.des(str({'status':'fail'}),key)
                conn.execute(" UPDATE Accounts SET Permissions =? WHERE User=?", ('Normal',str(Name),))
                return crypto2.des(str( {'status':'fail','reason':'return regular user'}),key)
        return  crypto2.des(str( {'status':'fail','reason':'dont have Permissions'}),key)

class GetUsersToReturn(Resource):
    def post(self):
        DATA=eval(crypto2.des_dicrypte((request.json['data']), key))
        conn = db_connect.connect()
        try:
            Name = DATA['User']
            if SubFunc.CheckAdmin(Name):
                query = conn.execute("select User from Accounts WHERE User<>? and Active=? ORDER BY Permissions ASC;", (str(Name),"False",))
                result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor],'status':'success'}
                return crypto2.des(str(result),key)
            return crypto2.des(str({'status':'haven\'t Permissions'}),key)
        except:
            return crypto2.des(str({'status':'fail'}),key)

class GetUsersToDelete(Resource):
    def post(self):
        DATA=eval(crypto2.des_dicrypte((request.json['data']), key))
        conn = db_connect.connect()
        try:
            Name = DATA['User']
            if SubFunc.CheckAdmin(Name):
                query = conn.execute("select User from Accounts WHERE User<>? and Active=? ORDER BY Permissions ASC;", (str(Name),"True",))
                result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor],'status':'success'}
                return crypto2.des(str(result),key)
            return  crypto2.des(str({'status':'haven\'t Permissions'}),key)
        except:
            return  crypto2.des(str({'status':'fail'}),key)

class GetUsersPerPermissions(Resource):
    def post(self):
        DATA=eval(crypto2.des_dicrypte((request.json['data']), key))
        conn = db_connect.connect()
        try:
            Name = DATA['User']
            Permissions=DATA['Permissions']
            if SubFunc.CheckAdmin(Name):
                query = conn.execute("select User from Accounts WHERE User<>? and Active=? and Permissions=? ORDER BY Permissions ASC;", (str(Name),"True",Permissions,))
                result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor],'status':'success'}
                return crypto2.des(str(result),key)
            return  crypto2.des(str({'status':'haven\'t Permissions'}),key)
        except:
            return  crypto2.des(str({'status':'fail'}),key)




class ReturnUser(Resource):
    def post(self):
        DATA=eval(crypto2.des_dicrypte((request.json['data']), key))
        conn = db_connect.connect()
        try:
            Name = DATA['User']
            if SubFunc.CheckAdmin(Name):
                Name = DATA['ReturnU']
                query = conn.execute("select * from Accounts WHERE User=? and Active=?", (str(Name),"False",))
                result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
                if not result['data']:
                    return crypto2.des(str({'status':'NoFind'}),key)
                conn.execute(" UPDATE Accounts SET Active =? WHERE User=?", ('True',str(Name),))
                return crypto2.des(str({'status':'success'}),key)
            return crypto2.des(str({'status':'fail'}),key)
        except:
            return  crypto2.des(str({'status':'fail'}),key)

class DeleteUser(Resource):
    def post(self):
        DATA=eval(crypto2.des_dicrypte(request.json['data'], key))
        conn = db_connect.connect()
        try:
            Name = DATA['User']
            if SubFunc.CheckAdmin(Name):
                Name = DATA['del']
                query = conn.execute("select * from Accounts WHERE User=? and Active=?", (str(Name),"True",))
                result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
                if not result['data']:
                    return crypto2.des(str({'status':'NoFind'}),key)
                conn.execute(" UPDATE Accounts SET Active =? WHERE User=?", ('False',str(Name),))
                return  crypto2.des(str({'status':'success'}),key)
            return crypto2.des(str({'status':'fail'}),key)
        except:
            return crypto2.des(str({'status':'fail'}),key)

class DeleteUserTast(Resource):
    def post(self):
        DATA=eval(crypto2.des_dicrypte(request.json['data'], key))
        conn = db_connect.connect()
        try:
            conn.execute("DELETE FROM Accounts WHERE User = ?;",(DATA['user'],))
            conn.execute("DELETE FROM LVL WHERE User = ?;",(DATA['user'],))
            conn.execute("DELETE FROM Profile WHERE UserName = ?;",(DATA['user'],))
            return crypto2.des(str({'status':'success'}),key)
        except:
            return crypto2.des(str({'status':'fail'}),key)


class UpdateProfile(Resource):
    def post(self):
        DATA=eval(crypto2.des_dicrypte(request.json['data'], key))
        try:
            conn = db_connect.connect()
            query = conn.execute("select * from Profile WHERE UserName=?", (DATA['user'],))
            result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
            if not result['data']:
                try:
                    conn.execute("insert into Profile values('{0}','{1}','{2}','{3}')".format(DATA['user'],DATA['email'],DATA['tel'],DATA['address']))
                    return crypto2.des(str({'status':'success','res':'new'}),key)
                except:
                    return crypto2.des(str({'status':'fail'}),key)
            else:
                if DATA['email']!='':
                    conn.execute(" UPDATE Profile SET email =?  WHERE UserName=?", (DATA['email'],DATA['user'],))
                if DATA['tel']!='':
                    conn.execute(" UPDATE Profile SET Tel =?  WHERE UserName=?", (DATA['tel'],DATA['user'],))
                if DATA['address']!='':
                    conn.execute(" UPDATE Profile SET address =?  WHERE UserName=?", (DATA['address'],DATA['user'],))
                return crypto2.des(str({'status':'success','res':'update'}),key)
        except:
            return crypto2.des(str({'status':'bug'}),key)


class ReturnProfile(Resource):
    def post(self):
        DATA=eval(crypto2.des_dicrypte((request.json['data']), key))
        try:
            conn = db_connect.connect()
            Name = DATA['User']
            query = conn.execute("select * from Profile WHERE UserName=?", (str(Name),))
            result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
            if not result['data']:
                return  crypto2.des(str({'status':'NoFind'}),key)
            return crypto2.des(str(result),key)
        except:
            return  crypto2.des(str({'status':'fail'}),key)

class trylogin(Resource):
    def post(self):
        DATA=eval(crypto2.des_dicrypte((request.json['data']), key))
        try:
            conn = db_connect.connect()
            Name = DATA['user']
            query = conn.execute("select * from Trylogin WHERE user=?", (Name,))
            result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
            date=datetime.datetime.now()
            if not result['data']:
                conn.execute("insert into Trylogin values('{0}','{1}','{2}','{3}')".format(DATA['user'],DATA['permissions'],DATA['key'],date))
                return crypto2.des(str({'status':'success','res':'new'}),key)
            else:
                conn.execute(" UPDATE Trylogin SET permissions=?,key=?,date=?  WHERE user=?", (DATA['permissions'],DATA['key'],date,Name,))
                return crypto2.des(str({'status':'success','res':'update'}),key)
        except:
            return crypto2.des(str({'status':'fail','res':'bug'}),key)


class login(Resource):
    def post(self):
        DATA=eval(crypto2.des_dicrypte((request.json['data']), key))
        try:
            conn = db_connect.connect()
            query = conn.execute("select * from Trylogin WHERE user=? and key=? ",(DATA['user'],DATA['Key'],))
            result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
            date=datetime.datetime.now()
            if not result['data']:
                return crypto2.des(str({'status':'fail','res':'Not find'}),key)
            else:
                try:
                    if(str(date).split(' ')[0]==result['data'][0]['date'].split(' ')[0]):
                        if(str(date).split(' ')[1].split(':')[0]==result['data'][0]['date'].split(' ')[1].split(':')[0]):
                            if((int(str(date).split(' ')[1].split(':')[1]) - int(result['data'][0]['date'].split(' ')[1].split(':')[1]))<10):
                                result['data'][0]['status']='success'
                                return crypto2.des(str(result['data'][0]),key)
                            else:
                                return crypto2.des(str({'status':'fail','res':'time over'}),key)
                        else:
                            return crypto2.des(str({'status':'fail','res':'not some houer'}),key)
                    else:
                        return crypto2.des(str({'status':'fail','res':'not some day'}),key)
                except:
                    return crypto2.des(str({'status':'fail','res':'date bug'}),key)
        except:
            return crypto2.des(str({'status':'fail','res':'bug'}),key)


class RequestPermissions(Resource):
    def post(self):
        DATA=eval(crypto2.des_dicrypte((request.json['data']), key))
        try:
            if (SubFunc.CheckAdmin(DATA['user']) or SubFunc.CheckManger(DATA['user'])) and SubFunc.CheckNormal(DATA['UserName']) :
                conn = db_connect.connect()
                query = conn.execute("select * from request WHERE requesting=? and user=? ",(DATA['user'],DATA['UserName'],))
                result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
                if len(result['data'])<3:
                    try:
                        conn.execute("insert into request (requesting, user, reason) values('{0}','{1}','{2}')".format(DATA['user'],DATA['UserName'],DATA['ReasonForRequest']))
                        return crypto2.des(str({'status':'success seve request'}),key)
                    except:
                        return crypto2.des(str({'status':'can\'t save request'}),key)
                else:
                    return crypto2.des(str({'status':'too mach request, pls wait for answer from admins '}),key)
            else:
                return crypto2.des(str({'status':'incorrect request, not save'}),key)
        except:
            return crypto2.des(str({'status':'can\'t find db'}),key)


class ReturnTrainee(Resource):
    def post(self):
        DATA=eval(crypto2.des_dicrypte((request.json['data']), key))
        conn = db_connect.connect()
        try:
            Name = DATA['User']
            if SubFunc.CheckAdmin(Name) or SubFunc.CheckManger(Name):
                query = conn.execute("select User from Guider WHERE GuideName =?;", (str(Name),))
                result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor],'status':'success'}
                return crypto2.des(str(result),key)
            return  crypto2.des(str({'status':'haven\'t Permissions'}),key)
        except:
            return  crypto2.des(str({'status':'fail'}),key)

class AddWord(Resource):
    def post(self):
        DATA=eval(crypto2.des_dicrypte((request.json['data']), key))
        conn = db_connect.connect()
        try:
            Name = DATA['User']
            if SubFunc.CheckAdmin(Name) or SubFunc.CheckManger(Name):
                try:
                    conn.execute("insert into '{2}' (user, reason) values('{0}','{1}')".format(DATA['trainee'],DATA['word'],DATA['language']))
                except:
                    return  crypto2.des(str({'status':'that word already exists'}),key)
                return crypto2.des(str({'status':'success'}),key)
            return  crypto2.des(str({'status':'haven\'t Permissions'}),key)
        except:
            return  crypto2.des(str({'status':'fail'}),key)


class getStudents(Resource):
    def post(self):
        DATA=eval(crypto2.des_dicrypte((request.json['data']), key))
        conn = db_connect.connect()
        try:
            user_Name = DATA['UserRequsting']
            if SubFunc.CheckAdmin(user_Name) or SubFunc.CheckManger(user_Name):
                try:
                    temp=[]
                    query = conn.execute("select user from Guider where GuideName==? and active='True';", (str(user_Name),))
                    for user in query.cursor:
                        temp+=user
                    result = {'data': temp,'status':'success'}
                    return crypto2.des(str(result),key)
                except:
                    return  crypto2.des(str({'status':'fail','code':'sqlfail'}),key)
                return  crypto2.des(str({'status':'haven\'t Permissions'}),key)
        except:
            return  crypto2.des(str({'status':'fail'}),key)


class getStudentsStatistics(Resource):
    def post(self):

        DATA=eval(crypto2.des_dicrypte((request.json['data']), key))

        conn = db_connect.connect()
        try:
            User = DATA['user']
            user_Name = DATA['user_serch']
            if SubFunc.CheckAdmin(user_Name) or SubFunc.CheckManger(user_Name):
                try:
                    temp=[]
                    query = conn.execute("select avg(grade) avrage from SpeechTasks WHERE  user==?", (str(user_Name),))
                    for user in query.cursor:
                        avrage=user.avrage
                    query = conn.execute("select Line,Say,grade,Date from SpeechTasks WHERE  user==?", (str(user_Name),))
                    for user in query.cursor:
                        temp+=[user.Line,user.Say,user.grade,user.Date]
                    result = {'data': temp,'status':'success','avrage':avrage}
                    return crypto2.des(str(result),key)
                except:
                    return  crypto2.des(str({'status':'fail','code':'sqlfail'}),key)
                return  crypto2.des(str({'status':'haven\'t Permissions'}),key)
        except:
            return  crypto2.des(str({'status':'fail'}),key)



api.add_resource(getStudents,  '/getstudents',methods={'POST','GET'})
api.add_resource(getStudentsStatistics,  '/getStudentsStatistics',methods={'POST','GET'})

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
api.add_resource(GetUsersPerPermissions, '/GetUsersPerPermissions',methods={'POST'})
api.add_resource(RequestPermissions, '/RequestPermissions',methods={'POST'})
api.add_resource(ReturnTrainee, '/trainee',methods={'POST'})
api.add_resource(AddWord, '/addword',methods={'POST'})

if __name__ == '__main__':
     app.run()
