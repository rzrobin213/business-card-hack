import json
from db import db, User
from flask import Flask, request


app = Flask(__name__)
db_filename = 'business.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/api/users/', methods=['GET'])
def get_all_users():
    users = User.query.all()
    res = {'success': True, 'data': [user.serialize(True) for user in users]}
    return json.dumps(res), 200


@app.route('/api/users/', methods=['POST'])
def create_user():
    user_dict = json.loads(request.data)
    print(user_dict)
    user_info = User(
        name=user_dict.get('name', "Robin Zheng"),
        email=user_dict.get('email', "rjz47@cornell.edu"),
        phone=user_dict.get('phone', "860-278-6106"),
        company=user_dict.get('company', "Cornell University"),
        imgURL=user_dict.get('imgURL', "feelsbad.jpg")
    )
    db.session.add(user_info)
    db.session.commit()
    return_info = {'success': True, 'data': user_info.serialize(True)}
    return json.dumps(return_info), 201


@app.route('/api/user/<int:user_id>/', methods=['GET'])
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is not None:
        return_suc = {'success': True, 'data': user.serialize(True)}
        return json.dumps(return_suc), 200
    return_fail = {'success': False, 'error': 'User not found!'}
    return json.dumps(return_fail), 404


@app.route('/api/user/<int:user_id>/', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is not None:
        db.session.delete(user)
        db.session.commit()
        return_suc = {'success': True, 'data': user.serialize(True)}
        return json.dumps(return_suc), 200
    return_fail = {'success': False, 'data': 'User not found'}
    return json.dumps(return_fail), 404


@app.route('/api/user/<int:user_id>/', methods=['PUT'])
def edit_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is not None:
        user_dict = json.loads(request.data)
        user.name = user_dict.get('name', user.name)
        user.email = user_dict.get('email', user.email)
        user.phone = user_dict.get('phone', user.phone)
        user.company = user_dict.get('company', user.company)
        user.imgURL = user_dict.get('imgURL', user.imgURL)
        db.session.commit()
        return_suc = {'success': True, 'data': user.serialize(True)}
        return json.dumps(return_suc), 200
    return_fail = {'success': False, 'data': 'User not found'}
    return json.dumps(return_fail), 404


@app.route('/api/user/<int:your_id>/<string:their_code>/', methods=['POST'])
def add_colleague(your_id, their_code):
    person = User.query.filter_by(id=your_id).first()
    contact = User.query.filter_by(code=their_code).first()
    if person is not None and contact is not None:
        person.contacts.append(contact)
        db.session.add(person)
        db.session.commit()
        return_suc = {'success': True, 'data': person.serialize(True)}
        return json.dumps(return_suc), 200
    return_fail = {'success': False, 'data': 'Person or code not found'}
    return json.dumps(return_fail), 404

@app.route('/api/user/<int:your_id>/<string:their_code>/', methods=['DELETE'])
def del_contact(your_id, their_code):
    person = User.query.filter_by(id=your_id).first()
    contact = User.query.filter_by(code=their_code).first()
    if person is not None and contact is not None:
        db.session.delete(contact)
        db.session.commit()
        return_suc = {'success': True, 'data': contact.serialize(True)}
        return json.dumps(return_suc), 200
    return_fail = {'success': False, 'data': 'contact not found'}
    return json.dumps(return_fail), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
