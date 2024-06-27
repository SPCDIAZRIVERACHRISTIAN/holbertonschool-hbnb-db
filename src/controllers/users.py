"""
Users controller module
"""

from src.persistence.db import DBRepository # Add this in every routes file
from persistence.__init__ import db_session # Add this in every routes file
from flask import abort, request
from src.models.user import User
from persistence.memory import MemoryRepository


db_repository = DBRepository(db_session)

def get_users():
    """Returns all users"""
    users: list[User] = User.get_all()

    return [user.to_dict() for user in users]


def create_user(): #use this function as an example to links the CRUD ops in other models and methods
    """
        Creates a new user and depending on what type
        type of storage it has it decides where to store it
    """
    data = request.get_json()

    try:
        if MemoryRepository.self.storage_type == 'database':
            user = db_repository.create(User, **data)
        elif MemoryRepository.self.storage_type == 'file':
            user = User.create(data)
    except KeyError as e:
        abort(400, f"Missing field: {e}")
    except ValueError as e:
        abort(400, str(e))

    if user is None:
        abort(400, "User already exists")

    return user.to_dict(), 201


def get_user_by_id(user_id: str):
    """Returns a user by ID"""
    user: User | None = User.get(user_id)

    if not user:
        abort(404, f"User with ID {user_id} not found")

    return user.to_dict(), 200


def update_user(user_id: str):
    """Updates a user by ID"""
    data = request.get_json()

    try:
        user = User.update(user_id, data)
    except ValueError as e:
        abort(400, str(e))

    if user is None:
        abort(404, f"User with ID {user_id} not found")

    return user.to_dict(), 200


def delete_user(user_id: str):
    """Deletes a user by ID"""
    if not User.delete(user_id):
        abort(404, f"User with ID {user_id} not found")

    return "", 204
