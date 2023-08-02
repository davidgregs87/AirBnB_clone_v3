#!/usr/bin/python3
"""a MODULE about building REST API
from the class REVIEW"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.review import Review
from models.user import User

@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['GET'])
def view_review_by_place_id(place_id):
    """Return all instance of review based on it's place id attribute"""
    review_list = []
    reviews = storage.all(Review).values()
    for review in reviews:
        if review.place_id == place_id:
            review_list.append(review.to_dict())
    if len(review_list) > 0:
        return jsonify(review_list)
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def view_review_by_review_id(review_id):
    """Return all instance of review based on it's review_id attribute"""
    reviews = storage.all(Review).values()
    for review in reviews:
        if review.id == review_id:
            return jsonify(review.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_review_by_review_id(review_id):
    """Delete an instance of Review based on it's review_id"""
    reviews = storage.all(Review).values()
    for review in reviews:
        if review.id == review_id:
            storage.delete(review)
            storage.save()
            return jsonify({}), 204
    abort(404)


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['POST'])
def create_review_by_place_id(place_id):
    """A function that create's a new review instance based on it's place_id"""
    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'text' not in request.get_json():
        abort(400, 'Missing text')
    data = request.get_json()
    user_id = data.get('user_id')
    place_id = place_id

    users = storage.all(User).values()
    for user in users:
        if user.id == user_id:
            data['place_id'] = place_id
            review = Review(**data)
            review.save()
            return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def update_review_by_review_id(review_id):
    """A function that update's a review instance based on it's review_id"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    reviews = storage.all(Review).values()
    for review in reviews:
        if review.id == review_id:
            data = request.get_json()
            for key, value in data.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(review, key, value)
            review.save()
            return jsonify(review.to_dict()), 200
    abort(404)
