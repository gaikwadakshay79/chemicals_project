from flask import Flask, request, abort, jsonify
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_authorize import Authorize
from functools import wraps
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chemicals.sqlite3'  
app.config['SECRET_KEY'] = "secret key" 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

import models

def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if request.headers.get('Authorization') is None and request.args.get('access_token') is None:
            abort(401)
        if request.headers.get('Authorization'):
            token = request.headers.get('Authorization')
        else:
            token = request.args.get('access_token')
        user = models.getUserByAccessToken(token)
        if user is None:
            abort(401)
        return f(user, *args, **kws)            
    return decorated_function

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

@app.route("/chemicals/get",methods= ["GET"] )
@authorize
def get_chemicals(user):
    return jsonify(models.getChemicals())

@app.route("/commodity/get",methods= ["GET"] )
@authorize
def get_commodities(user):
    return jsonify(models.getCommodities())

@app.route("/commodity/get/<id>",methods= ["GET"] )
@authorize
def get_commodity(user,id):
    commodity = models.getCommodityById(id)
    if commodity is None:
        abort(404)
    return jsonify(commodity)

@app.route("/commodity/update",methods= ["POST"] )
@authorize
def update_commodity(user):
    req_data = request.get_json()
    if req_data is not None and req_data.get('id') is not None:
        if req_data.get('name') or req_data.get('inventory') or req_data.get('price'):
            try:
                commodity = models.updateCommodity(req_data)
                if commodity is None:
                    abort(404)
            except:
                abort(405)
            return jsonify(commodity)
    return abort(405)

@app.route("/composition/remove/<cid>/<eid>",methods= ["POST"] )
@authorize
def remove_composition(user,cid,eid):
    success = models.removeComposition(cid,eid)
    if not success:
        abort(404)
    return json.dumps({'success':success}), 200, {'ContentType':'application/json'}

@app.route("/composition/update/<cid>/<eid>",methods= ["POST"] )
@authorize
def update_composition(user,cid,eid):
    req_data = request.get_json()
    if req_data is not None and req_data.get('percentage') is not None:
        success,data = models.addOrUpdateComposition(cid,eid,req_data.get('percentage'))
        if not success:
            abort(404)
        if not data:
            abort(406)
        return json.dumps(data), 200, {'ContentType':'application/json'}
    abort(405)

if __name__=='__main__':
    db.create_all()
    app.run(threaded=True, host='0.0.0.0', port=8080)