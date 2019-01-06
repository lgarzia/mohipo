from flask import jsonify
from . import api #global bluepoint

@api.route('users/<int:id>')
def get_user(id):
    user = {'userid': 25,
            'comment': 'hello world'}
    return jsonify(user)

#Task 2 -> Post
