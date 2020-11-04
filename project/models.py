
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

def getUserByAccessToken(access_token):
    access_token = db.session.query(AccessToken).filter_by(value = access_token).limit(1).first()
    user = None 
    if access_token is not None:
        user = access_token.person
    return user

def getChemicals():
    chemicals = db.session.query(Chemical).all()
    converter = lambda x : {'id' : x.id, 'name': x.name}
    chemicals = [converter(x) for x in chemicals]
    return chemicals

def getCommodities():
    commodities = db.session.query(Commodity).all()
    converter = lambda x : {'id' : x.id, 'name': x.name, 'inventory': x.inventory, 'price': x.price}
    commodities = [converter(x) for x in commodities]
    return commodities

def getCommodityById(id):
    commodities = db.session.query(Commodity).filter_by(id=id).first()
    resultToReturn = None
    if commodities is not None:
        resultToReturn = {}
        resultToReturn['id'] = commodities.id
        resultToReturn['name'] = commodities.name 
        resultToReturn['inventory'] = commodities.inventory
        resultToReturn['price'] = commodities.price
        resultToReturn['chemical_composition'] = []
        converter = lambda x : {'percentage' : x.percentage,'element' : {'id' : x.chemical.id, 'name': x.chemical.name}}
        s = 0
        for c in commodities.composition:
            n_c = converter(c)
            resultToReturn['chemical_composition'].append(n_c)
            s = s + c.percentage
        if s < 100:
            n_c = {}
            n_c['percentage'] = 100 - s
            n_c['element'] = {}
            n_c['element']['id'] = None
            n_c['element']['name'] = 'Unknown'
            resultToReturn['chemical_composition'].append(n_c)
    return resultToReturn

def updateCommodity(data):
    commodities = db.session.query(Commodity).filter_by(id=data.get('id')).first()
    if commodities is None:
        return None
    if data.get('name') is not None:
        commodities.name = data.get('name')
    if data.get('inventory') is not None:
        commodities.inventory = data.get('inventory')
    if data.get('price') is not None:
        commodities.price = data.get('price')
    db.session.commit()
    converter = lambda x : {'id' : x.id, 'name': x.name, 'inventory': x.inventory, 'price': x.price}
    c = converter(commodities)
    for i in ['name','inventory','price']:
        if data.get(i) is None:
            del c[i]
    return c 

def removeComposition(cid,eid):
    composition = db.session.query(Composition).filter_by(commodity_id = cid,chemical_id = eid).first()
    if composition is not None:
        db.session.delete(composition)
        db.session.commit()
        return True
    return composition

def addOrUpdateComposition(cid,eid,percentage):
    if type(percentage) not in (float, int):
        return True,False
    chemicals = db.session.query(Chemical).filter_by(id=eid).first()
    commodities = db.session.query(Commodity).filter_by(id=cid).first()
    if chemicals is None or commodities is None:
        return None,None
    composition = db.session.query(Composition).filter_by(commodity_id = cid,chemical_id = eid).first()
    updated = composition is not None
    s = 0
    for c in commodities.composition:
        s = s + c.percentage
    if updated:
        s = s - composition.percentage
    s = s + percentage
    if s>100:
        return True,False
    if updated:
        composition.percentage = percentage
    else:
        composition = Composition(chemical_id=eid,commodity_id=cid,percentage=percentage)
        db.session.add(composition)
    db.session.commit()
    converter = lambda x : {'element_id' : composition.chemical_id, 'commodity_id': composition.commodity_id, 'percentage': composition.percentage}
    return True,converter(composition)

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

class Chemical(db.Model):
    id = db.Column(db.String, primary_key=True, default=get_uuid , unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return "<Chemical (id='%s' ,name='%s')>" % (self.id ,self.name)

class Commodity(db.Model):
    id = db.Column(db.String, primary_key=True, default=get_uuid , unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    inventory = db.Column(db.Float, default=0, nullable=False)
    price = db.Column(db.Float, default=0,nullable=False)
    chemical = db.relationship(Chemical,secondary="composition")

    def __repr__(self):
        return "<Commodity (id='%s' ,name='%s' ,inventory='%s' ,price='%s')>" % (self.id ,self.name, self.inventory, self.price)

class Composition(db.Model):
    id = db.Column(db.String, primary_key=True, default=get_uuid , unique=True, nullable=False)
    chemical_id = db.Column(db.Integer, db.ForeignKey('chemical.id'),nullable=False)
    commodity_id = db.Column(db.Integer, db.ForeignKey('commodity.id'),nullable=False)
    percentage = db.Column(db.Float, default=0, nullable=False)
    chemical = db.relationship(Chemical, backref=db.backref("composition", cascade="all, delete-orphan"))
    commodity = db.relationship(Commodity, backref=db.backref("composition", cascade="all, delete-orphan"))
    def __repr__(self):
        return "<Composition (chemical_id='%s' ,commodity_id='%s' ,percentage='%s' )>" % (self.chemical_id ,self.commodity_id, self.percentage)
