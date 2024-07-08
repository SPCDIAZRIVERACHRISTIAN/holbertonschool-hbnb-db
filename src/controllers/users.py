"""
Users controller module
"""

from flask import abort, request, jsonify
from src.models.user import User
from flask_jwt_extended import jwt_required
from src.controllers.login import check_admin


def get_users():
    """Returns all users"""
    users: list[User] = User.get_all()

    return [user.to_dict() for user in users]

@jwt_required()
def create_user():
    """Creates a new user"""
    if check_admin() == True:
        data = request.get_json()

        try:
            user = User.create(data)
        except KeyError as e:
            abort(400, f"Missing field: {e}")
        except ValueError as e:
            abort(400, str(e))

        if user is None:
            abort(400, "User already exists")

        return user.to_dict(), 201
    else:
        return jsonify({'msg': 'Not allowed'}), 403


def get_user_by_id(user_id: str):
    """Returns a user by ID"""
    user: User | None = User.get(user_id)

    if not user:
        abort(404, f"User with ID {user_id} not found")

    return user.to_dict(), 200

@jwt_required()
def update_user(user_id: str):
    """Updates a user by ID"""
    if check_admin() == True:
        data = request.get_json()

        try:
            user = User.update(user_id, data)
        except ValueError as e:
            abort(400, str(e))

        if user is None:
            abort(404, f"User with ID {user_id} not found")

        return user.to_dict(), 200
    else:
        return jsonify({'msg': 'Not allowed'}), 403



@jwt_required()
def delete_user(user_id: str):
    """Deletes a user by ID"""
    if check_admin() == True:
        if not User.delete(user_id):
            abort(404, f"User with ID {user_id} not found")

        return "", 204
    else:
        return jsonify({'msg': 'Not allowed'}), 403
