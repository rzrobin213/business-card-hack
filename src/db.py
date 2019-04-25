from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() 

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False)
    phone = db.Column(db.String, nullable = False)
    company = db.Column(db.String, nullable = False)
    added = db.relationship('Colleagues', cascade = 'delete')

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', 'Anonymous')
        self.email = kwargs.get('email', '')
        self.phone = kwargs.get('phone', '')
        self.company = kwargs.get('company', '')


    def serialize(self):
        return {
        'id': self.id,
        'name': self.name,
        'email': self.email,
        'phone': self.phone,
        'company': self.company,
        'added': self.added
        }

class Colleagues(db.Model):
    __tablename__ = 'colleagues'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False)
    phone = db.Column(db.String, nullable = False)
    company = db.Column(db.String, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    friend_id = db.Column(db.Integer, nullable = False)


    def __init__(self, **kwargs):
        self.name = kwargs.get('name', 'Anonymous')
        self.email = kwargs.get('email', '')
        self.phone = kwargs.get('phone', '')
        self.company = kwargs.get('company', '')

    def serialize(self):
        return {
        'id': self.id,
        'friend_id': self.friend_id,
        'name': self.name,
        'email': self.email,
        'phone': self.phone,
        'company': self.company,
        }



