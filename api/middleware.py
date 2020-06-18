from functools import wraps


from flask import request, make_response, jsonify


def api_post_data_middleware():
    def _api_post_data_middleware(f):
        @wraps(f)
        def __api_post_data_middleware(*args, **kwargs):
            post_data = request.get_json()
            if post_data is None:
                response_object = {
                    'status': 'fail',
                    'message': 'Please provide json data.'
                }
                return make_response(jsonify(response_object), 400)
            else:
                return f(*args, **kwargs)
        return __api_post_data_middleware
    return _api_post_data_middleware
