
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



class Test(Resource):
    def get(self,Date,user):
        conn = db_connect.connect()
        query = conn.execute("select * from test where date=? and User_name=?",(Date,user,))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return Encryption.enc(str(result),key)

class PTest(Resource):
    def post(Self):
	    conn = db_connect.connect()
	    User = request.json['user']
	    if 'Date' in dict.keys():
	        Date = request.json['date']
	    else:
	        Date=datetime.datetime.now().strftime("%Y-%m-%d")
	    query = conn.execute("select * from test where date=? and User_name=?",(Line,User,))
	    result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
	    return Encryption.enc(str(result),key)


class STest(Resource):
    def post(self):
        conn = db_connect.connect()
        User = request.json['user']
        Line = request.json['line']
        Say = request.json['say']
        Date = datetime.datetime.now().strftime("%Y-%m-%d")
        query = conn.execute("insert into test values('{0}',null,'{1}','{2}','{3}')".format(User,Line,Say,Date))
        return {'status':'success'}




class Singin(Resource):
    def get(self, user,pas):
        conn = db_connect.connect()
        query = conn.execute("select * from account WHERE Name=?", (str(user),))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        if not result['data']:
            return {'status':'Ufail'}
        if(check_password_hash(result['data'][0]['Password'],pas)):
            return {'status':'success'}
        return {'status':'Pfail'}

class PSingin(Resource):
    def get(self):
        conn = db_connect.connect()
        user = request.json['user']
        pas = request.json['pas']
        query = conn.execute("select * from account WHERE Name=?", (str(user),))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        if not result['data']:
            return {'status':'Ufail'}
        if(check_password_hash(result['data'][0]['Password'],pas)):
            return {'status':'success'}
        return {'status':'Pfail'}

class singup(Resource):
    def post(self):
        conn = db_connect.connect()
        Name = request.json['Name']
        Password = request.json['Password']
        if len(Name)<2 or len(Password)<8 or Name.count("select")!=0:
            return {'status':'hacker'}
        query = conn.execute("select * from account WHERE Name=?", (str(Name),))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        if not result['data']:
        	query = conn.execute("insert into account values('{0}','{1}')".format(Name,generate_password_hash(Password, method='pbkdf2:sha256', salt_length=8)))
        	return {'status':'success'}
        return {'status':'fail'}


api.add_resource(Singin, '/singin/<user>/<pas>',methods={'POST','GET'})
api.add_resource(PSingin, '/singin',methods={'POST','GET'})
api.add_resource(Test, '/test/<user>/<Date>',methods={'POST','GET'})
api.add_resource(PTest, '/test',methods={'POST','GET'})
api.add_resource(STest, '/test',methods={'POST'})
api.add_resource(singup, '/singup',methods={'POST'})



if __name__ == '__main__':
     app.run()
