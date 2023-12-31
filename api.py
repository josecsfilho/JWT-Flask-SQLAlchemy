import os
from datetime import datetime
from functools import wraps

from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from passlib.hash import sha256_crypt  # Importe a função sha256_crypt do passlib
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


file_path = os.path.abspath(os.getcwd())+"/database.db" # permite criar o BD na raiz

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisissecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'

db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid! | Token é invalido'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)

    return jsonify({'users': output})

@app.route('/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user, public_id):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})


    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No  user found! | Nenhum usuário encontrado!'})

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin

    return jsonify({'user': user_data})

@app.route('/user', methods=['POST'])
@token_required
def create_user(current_user):

    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    data = request.get_json()

    hashed_password = sha256_crypt.hash(data['password'])  # Use sha256_crypt para gerar o hash da senha

    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    # Gerar um token JWT para o novo usuário criado
    access_token = create_access_token(identity=new_user.public_id)

    return jsonify({'message': 'New user created! | Novo usuário criado!', 'access_token': access_token}), 201
@app.route('/user/<public_id>', methods=['PUT'])
@token_required
def promote_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})


    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No  user found! | Nenhum usuário encontrado!'})

    user.admin = True
    db.session.commit()
    return jsonify({'message': 'The user has been promoted! | O usuário foi promovido!'})

@app.route('/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'No  user found! | Nenhum usuário encontrado!'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'The user has been deleted!'})

@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify | Não foi possível verificar', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.query.filter_by(name=auth.username).first()

    if not user:
        return make_response('Could not verify | Não foi possível verificar', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if auth and sha256_crypt.verify(auth.password, user.password):
        token = create_access_token(identity=auth.username)

        return jsonify({'token': token})

    return make_response('Could verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

@app.route('/todo', methods=['GET'])
@token_required
def get_all_todos(current_user):
    return ''

@app.route('/todo/<todo_id>', methods=['GET'])
@token_required
def get_one_todo(current_user, todo_id):
    return ''

@app.route('/todo', methods=['POST'])
@token_required
def create_todo(current_user, todo_id):
    data = request.get_json()

    new_todo = Todo(text=data['text'], complete=False, user_id=current_user)
    db.session.add(new_todo)
    db.session.commit()

    return jsonify({'message': 'Todo created! | Todo criado!'})

@app.route('/todo', methods=['PUT'])
@token_required
def complete_todo(current_user, todo_id):
    return ''

@app.route('/todo/<todo_id>', methods=['DELETE'])
@token_required
def delete_todo(current_user, todo_id):
    return ''


if __name__ == '__main__':
    with app.app_context():
        # Criar as tabelas no banco de dados
        db.create_all()
    app.run(debug=True)














