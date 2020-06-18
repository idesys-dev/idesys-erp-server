from flask import request, make_response, jsonify


from models.user import User


def authorization_middleware(request):
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
            return resp # return user id
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
