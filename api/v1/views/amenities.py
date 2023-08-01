#!/usr/bin/python3
"""a MODULE about building REST API
from the class AMENITY"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def view_amenities():
    """Return all amenities instances"""
    amenities = storage.all(Amenity).values()
    amen_list = []
    for amen in amenities:
        amen_list.append(amen.to_dict())
    return jsonify(amen_list)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['GET'])
def view_amenity_by_id(amenity_id):
    """Return an instance based on it's id"""
    amenities = storage.all(Amenity).values()
    for amen in amenities:
        if amen.id == amenity_id:
            return jsonify(amen.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_amenitiy_by_id(amenity_id):
    """Delete's an amenity based on it's id"""
    amenities = storage.all(Amenity).values()
    for amen in amenities:
        if amen.id == amenity_id:
            storage.delete(amen)
            storage.save()
            storage.close()
            return jsonify({})
    abort(404)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_amenity():
    """A function that create's new amenity object"""
    if 'name' not in request.get_json():
        raise make_response(jsonify({'error': 'Missing name'}), 400)
    if not request.get_json():
        raise make_response(jsonify({'error': 'Not a JSON'}), 400)
    new_state = Amenity(**request.get_json())
    storage.save()
    storage.close()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['PUT'])
def update_amenity(amenity_id):
    """A function to update current amenity instance"""
    if 'name' not in request.get_json():
        raise make_response(jsonify({'error': 'Missing name'}), 400)
    if not request.get_json():
        raise make_response(jsonify({'error': 'Not a JSON'}), 400)
    amenities = storage.all(Amenity).values()
    for amen in amenities:
        if amen.id == amenity_id:
            unpack = Amenity(**request.get_json())
            storage.save()
            storage.close()
            return jsonify(unpack.to_dict())
    abort(404)
