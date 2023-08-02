#!/usr/bin/python3
"""a MODULE about building REST API
from the class REVIEW"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['GET'])
def view_review_by_place_id(place_id):
    """Return all instance of review based on it's place id attribute"""
    review_list = []
    review = storage.get('Review', place_id)
    if review:
        review_list.append(review.to_dict())
        return jsonify(review_list)
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def view_review_by_review_id(review_id):
    """Return all instance of review based on it's review_id attribute"""
    review = storage.get('Review', review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_review_by_review_id(review_id):
    """Delete an instance of Review based on it's review_id"""
    review = storage.get('Review', review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 204
    else:
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
    user = storage.get('User', data['user_id'])
    if not user:
        abort(404)

    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def update_review_by_review_id(review_id):
    """A function that update's a review instance based on it's review_id"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    review = storage.get(Review, review_id)
    if review:
        data = request.get_json()
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(review, key, value)
                review.save()
                return jsonify(review.to_dict()), 200
    abort(404)
