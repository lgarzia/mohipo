from flask import jsonify, request, url_for
from . import api #global bluepoint

@api.route('users/<int:id>')
def get_user(id):
    user = {'userid': 25,
            'comment': 'hello world'}
    return jsonify(user)


#Task 2 -> Post
@api.route('users/user/', methods=['POST'])
def new_user():
    user = request.json
    print(user)
    return jsonify({"key": "value"}), 201, \
        {'Location': url_for('api.get_user', id=25, _external=True)}

