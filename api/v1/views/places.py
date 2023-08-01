#!/usr/bin/python3
"""a MODULE about building REST API
from the class AMENITY"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['GET'])
def view_place_by_city_id(city_id):
    """Return all list of places instance based on it's class_id"""
    places = storage.all(Place).values()
    place_list = []
    for place in places:
        if city_id in place.city_id:
            place_list.append(place.to_dict())
            return jsonify(place_list)
    abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def view_place_by_place_id(place_id):
    """Return a place instance based on it's place id"""
    places = storage.all(Place).values()
    for place in places:
        if place.id == place_id:
            return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_place_by_place_id(place_id):
    """Deletes a place instance based on it's place id"""
    places = storage.all(Place).values()
    for place in places:
        if place.id == place_id:
            storage.delete(place)
            storage.save()
            storage.close()
            return jsonify({})
    abort(404)


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['POST'])
def create_place(city_id):
    """Create a new place instance"""
    if 'user_id' not in request.get_json():
        raise make_response(jsonify({'error': 'Missing user_id'}), 400)
    if not request.get_json():
        raise make_response(jsonify({'error': 'Not a JSON'}), 400)
    places = storage.all(Place).values()
    for place in places:
        if place.city_id == city_id:
            unpack = Place(**request.get_json())
            return jsonify(unpack.to_dict()), 201
    abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    """Update a place instance"""
    if not request.get_json():
        raise make_response(jsonify({'error': 'Not a JSON'}), 400)
    places = storage.all(Place).values()
    for place in places:
        if place.id == place_id:
            unpack = Place(**request.get_json())
            return jsonify(unpack.to_dict())
    abort(404)
