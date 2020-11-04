from app import db 
from models import *
if __name__ == "__main__":
    db.create_all()
    if db.session.query(Person).filter_by(username='admin').first() is None:
        person = Person(password='admin', username='admin')
        db.session.add(person)
        db.session.commit()
    print(db.session.query(Person).all())