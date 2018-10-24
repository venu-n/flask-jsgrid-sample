## device_control/reference.py  ##

from flask import Flask, jsonify, request, make_response, render_template
from flask_sqlalchemy import SQLAlchemy
import uuid
import datetime
from functools import wraps
import jwt
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = "MySecretKey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../instance/flask-crud.db"

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)
    is_delete = db.Column(db.Boolean)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/user', methods=['GET'])
#def get_all_users(current_user, pub_id):
def get_all_users():
    users = User.query.all()
    output = []
    for user in users:
        # user_data = {}
        # user_data['public_id'] = user.public_id
        # user_data['name'] = user.name
        # user_data['password'] = user.password
        # user_data['admin'] = user.admin
        # output.append(user_data)
        output.append({
        'ID':user.public_id,
        'UserName':user.name,
        'Psswd':user.password,
        'isAdmin':user.admin})

    return jsonify(output)

@app.route('/user/<public_id>', methods=['GET'])
def get_one_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    # user_data = {}
    # user_data['public_id'] = user.public_id
    # user_data['name'] = user.name
    # user_data['password'] = user.password
    # user_data['admin'] = user.admin
    new_user = []
    new_user.append({
    'ID':user.public_id,
    'UserName':user.name,
    'Psswd':user.password,
    'isAdmin':user.admin})
    print(new_user)
    #return jsonify([user_data]})
    #return jsonify({"data":new_user})
    return jsonify(new_user)

@app.route('/user', methods=['POST'])
def create_user():
    #data = request.get_json()

    pub_id = str(uuid.uuid4())
    hashed_password = generate_password_hash(request.form['Psswd'],method='sha256')

    new_user = User(public_id=pub_id, name=request.form['UserName'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    user = User.query.filter_by(public_id=pub_id).first()
    new_user = []
    new_user.append({
        'ID':user.public_id,
        'UserName':user.name,
        'Psswd':user.password,
        'isAdmin':user.admin})
    print(new_user)
    return jsonify(new_user)

    #return jsonify({'message': 'New user created!'})


@app.route('/user/<public_id>', methods=['PUT'])
def promote_user(current_user, public_id, pub_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    user.admin = True
    db.session.commit()

    return jsonify({'message': 'The user has been promoted!'})


@app.route('/user/<public_id>', methods=['DELETE'])
def delete_user(public_id):

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'The user has been deleted!'})


if __name__ == "__main__":
    app.run(debug=True)