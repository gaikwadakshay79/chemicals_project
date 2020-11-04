from app import db 
from models import *
import pandas as pd

def add_user():
    if db.session.query(Person).filter_by(username='admin').first() is None:
        person = Person(password='admin', username='admin')
        db.session.add(person)
        db.session.commit()

def add_chemicals():
    if db.session.query(Commodity).first() is not None:
        return
    df = pd.read_csv('./project/migratedata.csv')
    chemical_dict = {}
    commodity_dict = {}
    df = df.set_index('elements')
    for c in df.columns.tolist():
        name = c 
        inventory = df[c].loc['inventory']
        price = df[c].loc['price']
        currentCommodity = Commodity(name = name,inventory = inventory, price=price)
        db.session.add(currentCommodity)
        db.session.commit()
        commodity_dict.update({c:currentCommodity.id})
    elements = [e for e in df.index.tolist() if e not in ['inventory','price']]
    for e in elements:
        name = e
        currentChemical = Chemical(name = name)
        db.session.add(currentChemical)
        db.session.commit()
        chemical_dict.update({e:currentChemical.id})
    df = df.to_dict('index')
    for e in elements:
        for c in df.get(e):
            if df[e][c]>0:
                cid = commodity_dict.get(c)
                eid = chemical_dict.get(e)
                comp = Composition(chemical_id=eid,commodity_id=cid,percentage=df[e][c])
                db.session.add(comp)
                db.session.commit()

def migrate():
    db.create_all()
    add_user()
    add_chemicals()

if __name__ == "__main__":
    migrate()