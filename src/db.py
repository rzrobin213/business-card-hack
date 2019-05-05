import uuid
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
# A person (of type user) can have many friends. (who are also of type user).
user_contact_assoc_table = db.Table(
    'user_contact',
    db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('contact_id', db.Integer, db.ForeignKey('user.id'))
)
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    company = db.Column(db.String, nullable=False)
    code = db.Column(db.String, nullable=False)
    imgURL = db.Column(db.String, nullable=False)
    position = db.Column(db.String, nullable=False)
    website = db.Column(db.String, nullable=False)
    contacts = db.relationship(
        'User',
        secondary=user_contact_assoc_table,
        primaryjoin=id == user_contact_assoc_table.c.user_id,
        secondaryjoin=id == user_contact_assoc_table.c.contact_id,
        backref=db.backref('following')
    )
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', 'Rodrigo Taipe')
        self.email = kwargs.get('email', 'rt363@cornell.edu')
        self.phone = kwargs.get('phone', '201-598-3168')
        self.company = kwargs.get('company', 'Cornell University')
        self.position = kwargs.get('position', 'Student')
        self.website = kwargs.get('website', 'rodrigotaipe.me')
        self.code = uuid.uuid4().hex[:6].upper()
        self.imgURL = kwargs.get(
            'imgURL', 'https://specials-images.forbesimg.com/imageserve/559d31a2e4b05c2c3431bde9/300x300.jpg?fit=scale&background=000000')
    def serialize(self, toplevel):
        if toplevel:
            return {
                'id': self.id,
                'name': self.name,
                'phone': self.phone,
                'email': self.email,
                'company': self.company,
                'code': self.code,
                'imgURL': self.imgURL,
                'position': self.position,
                'website': self.website,
                'contacts': [u.serialize(False) for u in self.contacts]
            }
        else:
            return {
                'id': self.id,
                'name': self.name,
                'phone': self.phone,
                'email': self.email,
                'company': self.company,
                'code': self.code,
                'imgURL': self.imgURL,
                'position': self.position,
                'website': self.website,
                'contacts': []
            }