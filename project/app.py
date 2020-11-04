from flask import Flask, request
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_authorize import Authorize
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.sqlite3'  
app.config['SECRET_KEY'] = "secret key" 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

import models


@app.route("/login",methods= ["POST"] )
def sign_in():
    req_data = request.get_json()
    if req_data is not None and 'username' in req_data and 'password' in req_data:
        access_token = models.login(req_data.get('username'),req_data.get('password'))
        if access_token is not None:
            return json.dumps({'success':True, 'access_token':access_token}), 200, {'ContentType':'application/json'}
        return "USERNAME_OR_PASSWORD_NOT_FOUND", 404, {'ContentType':'application/json' }
    return "METHOD_NOT_ALLOWED", 405, {'ContentType':'application/json'} 


@app.route("/logout",methods= ["POST"] )
def sign_out():
    req_data = request.get_json()
    if req_data is not None and 'access_token' in req_data:
        models.logout(req_data.get('access_token'))
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    return "METHOD_NOT_ALLOWED", 405, {'ContentType':'application/json'} 

if __name__=='__main__':
    app.run()