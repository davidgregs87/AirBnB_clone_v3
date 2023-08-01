#!/usr/bin/python3
"""A module that takes care of City class
of the REST API"""
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import jsonify, abort, request, make_response


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['GET'])
def view_cities_by_state_id(state_id):
    """Returns the dictionary of all city instances"""
    city = storage.get(City, state_id)
    city_list = []
    if city:
        city_list.append(city.to_dict())
        return jsonify(city_list)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def view_city(city_id):
    """Retrieve a city based on it's id"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """Delete a city instance based on it's id"""
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['POST'])
def create_city(state_id):
    """Creates a new state instanced based on it's
    state's id"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)

    data = request.get_json()
    cities = storage.all(City).values()
    for city in cities:
        if city.state_id == state_id:
            unpack_city = City(**data)
            return jsonify(unpack_city.to_dict()), 201
    abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """update an existing city instance based on it's id"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)

    data = request.get_json()
    cities = storage.all(City).values()
    for city in cities:
        if city.id == city_id:
            unpack_city = City(**data)
            return jsonify(unpack_city.to_dict()), 200
    abort(404)
