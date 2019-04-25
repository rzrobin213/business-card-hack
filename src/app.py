import json
from db import db, User, Colleagues
from flask import Flask, request


app = Flask(__name__)
db_filename = 'business.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/api/users/')
def get_all_users():
    users = User.query.all()
    res = {'success': True, 'data': [user.serialize() for user in users]}
    return json.dumps(res), 200
    
@app.route('/api/users/', methods = ['POST'])
def create_user():
    user_dict = json.loads(request.data)
    
    user_info = User(
        name = user_dict.get('name',"anon"),
        email = user_dict.get('email',""),
        phone = user_dict.get('phone',""),
        company = user_dict.get('company',""),
    )
    db.session.add(user_info)
    db.session.commit()
    return_info = {'success': True, 'data': user_info.serialize()}
    return json.dumps(return_info), 201

@app.route('/api/user/<int:user_id>/')
def get_user(user_id):
    user = User.query.filter_by(id = user_id).first()
    if user is not None:
        return_suc = {'success': True, 'data': user.serialize()}
        return json.dumps(return_suc), 200
    return_fail = {'success': False, 'error': 'Post not found!'}
    return json.dumps(return_fail), 404

@app.route('/api/user/<int:user_id>/', methods = ['DELETE'])
def delete_user(user_id):
    user = User.query.filter_by(id = user_id).first() 
    if user is not None:
        db.session.delete(user)
        db.session.commit()
        return_suc = {'success': True, 'data': user.serialize()}
        return json.dumps(return_suc), 200
    return_fail = {'success': False, 'data': 'Post not found'}
    return json.dumps(return_fail), 404

@app.route('/api/user/<int:user_id>/', methods = ['POST'])
def edit_user(user_id):
    user = User.query.filter_by(id = user_id).first() 
    if user is not None:
        user_dict = json.loads(request.data)
        user.name = user_dict.get('name',user.name)
        user.email = user_dict.get('email',user.email)
        user.phone = user_dict.get('phone',user.phone)
        user.company = user_dict.get('company',user.company)
        db.session.commit()
        return_suc = {'success': True, 'data': user.serialize()}
        return json.dumps(return_suc), 200
    return_fail = {'success': False, 'data': 'Post not found'}
    return json.dumps(return_fail), 404

@app.route('/api/user/<int:uniq_id>/<int:other_id>/colleague/', methods = ['POST'])
def add_colleague(uniq_id,other_id):
    person = User.query.filter_by(id = uniq_id).first() 
    if person is not None:
        friend = User.query.filter_by(id = other_id).first()
        colleague = Colleagues(
            name = friend.name,
            email = friend.email,
            phone = friend.phone,
            company = friend.company,
            user_id = person.id,
            friend_id = friend.id,
        )
        user.added.append(colleague)
        db.session.add(colleague)
        db.session.commit()
        return_suc = {'success': True, 'data': comment.serialize()}
        return json.dumps(return_suc), 200
    return_fail = {'success': False, 'data': 'Post not found'}
    return json.dumps(return_fail), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
