"""
Amenity controller module
"""

from flask import abort, request, jsonify
from src.controllers.login import check_admin
from src.models.amenity import Amenity
from flask_jwt_extended import jwt_required


def get_amenities():
    """Returns all amenities"""
    amenities: list[Amenity] = Amenity.get_all()

    return [amenity.to_dict() for amenity in amenities]


def create_amenity():
    """Creates a new amenity"""

    if check_admin() == True:
        data = request.get_json()

    try:
        amenity = Amenity.create(data)
    except KeyError as e:
        abort(400, f"Missing field: {e}")
    except ValueError as e:
        abort(400, str(e))

    return amenity.to_dict(), 201


def get_amenity_by_id(amenity_id: str):
    """Returns a amenity by ID"""
    amenity: Amenity | None = Amenity.get(amenity_id)

    if not amenity:
        abort(404, f"Amenity with ID {amenity_id} not found")

    return amenity.to_dict()


def update_amenity(amenity_id: str):
    """Updates a amenity by ID"""
    if check_admin() == True:
        data = request.get_json()

    updated_amenity: Amenity | None = Amenity.update(amenity_id, data)

    if not updated_amenity:
        abort(404, f"Amenity with ID {amenity_id} not found")

    return updated_amenity.to_dict()


def delete_amenity(amenity_id: str):
    """Deletes a amenity by ID"""
    if check_admin() == True:
        if not Amenity.delete(amenity_id):
              abort(404, f"Amenity with ID {amenity_id} not found")

        return "", 204
    else:
        return jsonify({'msg': 'Not allowed'}), 403
