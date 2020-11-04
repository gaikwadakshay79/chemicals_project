
from app import db 
import uuid
import random 
import string

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def random_string(length = 80):
    ans = get_random_string(length)
    while db.session.query(AccessToken).filter_by(value = ans).limit(1).first() is not None:
        ans = get_random_string(length)
    return ans

def get_uuid():
    return str(uuid.uuid4())

def login(username,password):
    access_token = None
    user = db.session.query(Person).filter_by(username = username, password = password).limit(1).first()
    if  user is not None:
        a_t = AccessToken(person_id=user.id)
        db.session.add(a_t)
        db.session.commit()
        access_token = a_t.value
    return access_token

def logout(access_token):
    access_token = db.session.query(AccessToken).filter_by(value = access_token).limit(1).first()
    if access_token is not None:
        db.session.delete(access_token)
        db.session.commit()

class Person(db.Model):
    id = db.Column(db.String, primary_key=True, default=get_uuid , unique=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    tokens = db.relationship('AccessToken', backref='person', lazy=True)

    def __repr__(self):
        return "<Person (id='%s' ,username='%s', password='%s')>" % (self.id ,self.username, self.password)

class AccessToken(db.Model):
    id = db.Column(db.String, primary_key=True, default=get_uuid , unique=True, nullable=False)
    value = db.Column(db.String(80), default=random_string, nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'),nullable=False)

    def __repr__(self):
        return "<AccessToken (id='%s' ,value='%s', person_id='%s')>" % (self.id ,self.value, self.person_id)
