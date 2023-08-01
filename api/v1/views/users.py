#!/usr/bin/python3
"""a MODULE about building REST API
from the class AMENITY"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def view_users():
    """Return all user instances"""
    users = storage.all(User).values()
    user_list = []
    for user in users:
        user_list.append(user.to_dict())
    return jsonify(user_list)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def view_user_by_id(user_id):
    """Return an instance based on it's id"""
    users = storage.all(User).values()
    for user in users:
        if user.id == user_id:
            return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['DELETE'])
def delete_user_by_id(user_id):
    """Delete's a user based on it's id"""
    users = storage.all(User).values()
    for user in users:
        if user.id == user_id:
            storage.delete(user)
            storage.save()
            storage.close()
            return jsonify({})
    abort(404)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """A function that create's new amenity object"""
    if 'name' not in request.get_json():
        raise make_response(jsonify({'error': 'Missing name'}), 400)
    if not request.get_json():
        raise make_response(jsonify({'error': 'Not a JSON'}), 400)
    new_user = User(**request.get_json())
    storage.save()
    storage.close()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    """A function to update current amenity instance"""
    if 'name' not in request.get_json():
        raise make_response(jsonify({'error': 'Missing name'}), 400)
    if not request.get_json():
        raise make_response(jsonify({'error': 'Not a JSON'}), 400)
    users = storage.all(User).values()
    for user in users:
        if user.id == user_id:
            unpack = User(**request.get_json())
            storage.save()
            storage.close()
            return jsonify(unpack.to_dict())
    abort(404)
