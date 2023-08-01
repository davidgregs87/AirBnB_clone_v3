#!/usr/bin/python3
"""Create a new view for State objects that
handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.state import State
from models import storage


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def view_states():
    """List all states"""
    states = storage.all(State).values()
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def view_states_by_id(state_id):
    """with state_id retrieves a State object"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_state_by_id(state_id):
    """Delete a state instance by it's id"""
    states = storage.all(State).values()
    for state in states:
        if state.id == state_id:
            storage.delete(state)
            storage.save()
            return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/', strict_slashes=True, methods=['POST'])
def create_state():
    """Creates a State"""
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    if not request.get_json():
        abort(400, 'Not a JSON')
    new_state = State(**request.get_json())
    # Save the new State instance to the storage
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """update a state"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    states = storage.all(State).values()
    for state in states:
        if state.id == state_id:
            data = request.get_json()
            for key, value in data.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(state, key, value)
                    state.save()
                return jsonify(state.to_dict()), 200
    abort(404)
