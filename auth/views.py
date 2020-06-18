"""
https://realpython.com/token-based-authentication-with-flask/#sanity-check
"""


from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
import bcrypt


from models.user import User
from models.black_list_token import BlacklistToken


auth_blueprint = Blueprint('auth', __name__)


class RegisterAPI(MethodView):
    """
    User Registration Resource
    """

    def post(self):
        # get the post data
        post_data = request.get_json()
        # check if user already exists
        user = User.objects(email=post_data.get('email'))
        if not user:
            if not post_data.get('email').endswith('@idesys.org'):
                response_object = {
                    'status': 'error',
                    'message': 'Email is not in the domain.',
                }
                return make_response(jsonify(response_object), 400)
            try:
                user = User(
                    email=post_data.get('email'),
                    password_hash=bcrypt.hashpw(post_data.get('password').encode(), bcrypt.gensalt()),
                    can_validate=False
                )

                # insert the user
                user.save()
                # generate the auth token
                auth_token = user.encode_auth_token(user.id)
                response_object = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode(),
                    'user': user
                }
                return make_response(jsonify(response_object), 201)
            except Exception as e:
                print(__name__, 54, e)
                response_object = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(response_object), 401)
        else:
            response_object = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return make_response(jsonify(response_object), 202)


class LoginAPI(MethodView):
    """
    User Login Resource
    """
    def post(self):
        # get the post data
        post_data = request.get_json()
        try:
            # fetch the user data
            user = User.objects(email=post_data.get('email')).first()
            if user and bcrypt.checkpw(post_data.get('password').encode(), user.password_hash.encode()):
                auth_token = user.encode_auth_token(user.id)
                if auth_token:
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token.decode(),
                        'user': user
                    }
                    return make_response(jsonify(response_object), 200)
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'User does not exist or invalid password.'
                }
                return make_response(jsonify(response_object), 404)
        except Exception as e:
            print(__name__, 82, e)
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(response_object), 500)


class UserAPI(MethodView):
    """
    User Resource
    """
    def get(self):
        # get the auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                response_object = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return make_response(jsonify(response_object), 401)
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if 'Error' not in resp:
                user = User.objects(id=resp).first()
                response_object = {
                    'status': 'success',
                    'data': {
                        'user_id': str(user.id),
                        'email': user.email,
                        'can_validate': user.can_validate,
                    }
                }
                return make_response(jsonify(response_object), 200)
            response_object = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(response_object), 401)
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(response_object), 401)


class LogoutAPI(MethodView):
    """
    Logout Resource
    """
    def post(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if 'Error' not in resp:
                # mark the token as blacklisted
                blacklist_token = BlacklistToken.new_black_list_token(token=auth_token)
                try:
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully logged out.'
                    }
                    return make_response(jsonify(response_object), 200)
                except Exception as e:
                    print(__name__, 157, e)
                    response_object = {
                        'status': 'fail',
                        'message': e
                    }
                    return make_response(jsonify(response_object), 200)
            else:
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return make_response(jsonify(response_object), 401)
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(response_object), 403)

# define the API resources
registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')
user_view = UserAPI.as_view('user_api')
logout_view = LogoutAPI.as_view('logout_api')

# add Rules for API Endpoints
auth_blueprint.add_url_rule(
    '/register',
    view_func=registration_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/login',
    view_func=login_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/status',
    view_func=user_view,
    methods=['GET']
)
auth_blueprint.add_url_rule(
    '/logout',
    view_func=logout_view,
    methods=['POST']
)
