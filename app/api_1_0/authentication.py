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
    if email == 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTU0NjkxMDc2MSwiZXhwIjoxNTQ2OTE0MzYxfQ.eyJlbWFpbCI6Ikx1a2UifQ.sg_aReO8z-Ak6r3hc3BV__052ZpUfgZwpzlbAGeafa1R11WsYpqsJEKN0X_99Gkb30JJQ8i44msSmV_rB5DY2w':
        g.current_user = 'Luke'
        return True
    if password=='luke' and email== 'luke':
        print(f"Not Luke's Email")
        g.current_user = 'Luke'
        return True #-> triggers the @auth.error_handler
    else:
        print(f"Luke's Email")
        return False


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


# Try building bare bones Token Based Authentication
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


# Part 1-> get token
@api.route('/token')
def get_token():
    print('in getting token')
    if g.current_user == 'Luke':
        s = Serializer('My Secret Key', 3600)
        token = s.dumps({'email': 'Luke'}).decode('utf-8')
        return jsonify({'token': token, 'expiration': 3600})
