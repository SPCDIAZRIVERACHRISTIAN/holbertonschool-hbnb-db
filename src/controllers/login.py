from flask import request, jsonify
from src.models.user import User
from src import bcrypt
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return 'Wrong username or password', 401

@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
