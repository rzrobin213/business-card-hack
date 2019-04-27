import uuid
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() 

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False)
    phone = db.Column(db.String, nullable = False)
    company = db.Column(db.String, nullable = False)
    code = db.Column(db.String, nullable=False)
    imgURL = db.Column(db.String, nullable=False)
    contacts = db.relationship('Associates', cascade = 'delete')

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', 'Anonymous')
        self.email = kwargs.get('email', '')
        self.phone = kwargs.get('phone', '')
        self.company = kwargs.get('company', '')
        self.code = uuid.uuid4().hex[:6].upper()
        self.imgURL = kwargs.get('imgURL', '')

    def serialize(self):
        return {
        'id': self.id,
        'name': self.name,
        'email': self.email,
        'phone': self.phone,
        'company': self.company,
        'contacts': self.contacts,
        'code': self.code,
        'imgURL': self.imgURL,
        'contacts': [c.serialize() for c in self.contacts]
        }

class Associates(db.Model):
    __tablename__ = 'associates'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False)
    phone = db.Column(db.String, nullable = False)
    company = db.Column(db.String, nullable = False)
    code = db.Column(db.String, nullable=False)
    imgURL = db.Column(db.String, nullable=False)
    their_code = db.Column(db.String, db.ForeignKey('user.code'), nullable = False)


    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.email = kwargs.get('email', '')
        self.phone = kwargs.get('phone', '')
        self.company = kwargs.get('company', '')
        self.code = kwargs.get('code', '')
        self.imgURL = kwargs.get('imgURL', '')

    def serialize(self):
        return {
        'id': self.id,
        'code': self.code,
        'name': self.name,
        'email': self.email,
        'phone': self.phone,
        'company': self.company,
        'imgURL': self.imgURL
        }

