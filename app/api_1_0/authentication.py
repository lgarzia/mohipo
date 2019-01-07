from . import api
from flask import g, jsonify
from ..models import User
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()
#HTTP Authentication; Send Credentials; Send Authorization Header


@auth.verify_password
def verify_password(email, password):
    print(email, password)
    if email == '':
        print(f"in empty email")
        g.current_user = None #AnonymousUser()
        return True
    if email != 'luke':
        print(f"Not Luke's Email")
        return False #-> triggers the @auth.error_handler
    else:
        print(f"Luke's Email")
        g.current_user = 'Luke'
        return True


@auth.error_handler
def auth_error():
    response = jsonify({'error': 'unauthorized', 'message': 'Invalid Credentials'})
    response.status_code = 401
    return response


# register handler with blueprint
@api.before_request
@auth.login_required #-> if return False -> goes to auth_error() function -> sets the g.current_user
def before_request():
    if g.current_user != 'Luke':
        response = jsonify({'error': 'unauthorized', 'message': 'Forbidden'})
        response.status_code = 401
        return response

