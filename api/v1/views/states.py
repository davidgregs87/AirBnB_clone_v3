#!/usr/bin/python3
"""Create a new view for State objects that
handles all default RESTFul API actions"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.state import State
from models import storage

classes = {"State": State}


@app_views.route('/states', methods=['GET'])
def view_states():
    """List all states"""
    states = storage.all(State).values()
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def view_states_by_id(state_id):
    """with state_id retrieves a State object"""
    states = storage.all(State).values()
    for state in states:
        if state.id == state_id:
            return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state_by_id(state_id):
    """Delete a state instance by it's id"""
    states = storage.all(State).values()
    for state in states:
        if state.id == state_id:
            storage.delete(state)
            storage.save()
            storage.close()
            return jsonify({})
    abort(404)


@app_views.route('/states/', strict_slashes=True, methods=['POST'])
def create_state():
    """Creates a State"""
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    new_state = State(**request.get_json())
    # Save the new State instance to the storage

    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """update a state"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(state, attr, val)
    return jsonify(state.to_dict())
