
from flask import Flask, request, jsonify, Blueprint, g, redirect, render_template, session, url_for
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
import Encryption
from werkzeug.security import check_password_hash, generate_password_hash

db_connect = create_engine('sqlite:///nedd.db')
app = Flask(__name__)
api = Api(app)




class Tast(Resource):
    def get(self,Date="date(now)"):
        conn = db_connect.connect()
        query = conn.execute("select * from tast where date=?",(Date,))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return Encryption.enc(str(result),"NEDD")

    def post(self):
        conn = db_connect.connect()
        print(request.json)
        LastName = request.json['LastName']
        FirstName = request.json['FirstName']
        Title = request.json['Title']
        ReportsTo = request.json['ReportsTo']
        BirthDate = request.json['BirthDate']
        HireDate = request.json['HireDate']
        Address = request.json['Address']
        City = request.json['City']
        State = request.json['State']
        Country = request.json['Country']
        PostalCode = request.json['PostalCode']
        Phone = request.json['Phone']
        Fax = request.json['Fax']
        Email = request.json['Email']
        query = conn.execute("insert into employees values(null,'{0}','{1}','{2}','{3}', \
                             '{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}', \
                             '{13}')".format(LastName,FirstName,Title,
                             ReportsTo, BirthDate, HireDate, Address,
                             City, State, Country, PostalCode, Phone, Fax,
                             Email))
        return {'status':'success'}


class Singin(Resource):
    def get(self, user,pas):
        conn = db_connect.connect()
        query = conn.execute("select * from account WHERE Name=? AND Password=?", (str(user),str(pas),))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return Encryption.enc(str(result),"NEDD")


api.add_resource(Singin, '/singin/<user>/<pas>') # Route_3
api.add_resource(Tast, '/tast/<Date>') # Route_3



if __name__ == '__main__':
     app.run()
