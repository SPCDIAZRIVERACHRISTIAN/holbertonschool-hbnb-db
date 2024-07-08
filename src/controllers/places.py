"""
Places controller module
"""

from flask import abort, request, jsonify
from src.models.place import Place
from flask_jwt_extended import jwt_required
from src.controllers.login import check_admin


def get_places():
    """Returns all places"""
    places: list[Place] = Place.get_all()

    return [place.to_dict() for place in places], 200

@jwt_required()
def create_place():
    """Creates a new place"""
    if check_admin() == True:
        data = request.get_json()

        try:
            place = Place.create(data)
        except KeyError as e:
            abort(400, f"Missing field: {e}")
        except ValueError as e:
            abort(404, str(e))

        return place.to_dict(), 201
    else:
        return jsonify({'msg': 'Not allowed'}), 403


def get_place_by_id(place_id: str):
    """Returns a place by ID"""
    place: Place | None = Place.get(place_id)

    if not place:
        abort(404, f"Place with ID {place_id} not found")

    return place.to_dict(), 200

@jwt_required()
def update_place(place_id: str):
    """Updates a place by ID"""
    if check_admin() == True:
        data = request.get_json()

        try:
            place: Place | None = Place.update(place_id, data)
        except ValueError as e:
            abort(400, str(e))

        if not place:
            abort(404, f"Place with ID {place_id} not found")

        return place.to_dict(), 200
    else:
        return jsonify({'msg': 'Not allowed'}), 403


@jwt_required()
def delete_place(place_id: str):
    """Deletes a place by ID"""
    if check_admin() == True:
        if not Place.delete(place_id):
            abort(404, f"Place with ID {place_id} not found")

        return "", 204
    else:
        return jsonify({'msg': 'Not allowed'}), 403
