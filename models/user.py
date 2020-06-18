import datetime
import os


import mongoengine as me
import bcrypt
import jwt


from models.black_list_token import BlacklistToken


with open('flask.secret') as my_file:
    SECRET_KEY = my_file.read().strip()


class User(me.Document):
    email = me.EmailField(required=True)
    password_hash = me.StringField(required=True)
    can_validate = me.BooleanField()

    @staticmethod
    def encode_auth_token(user_id):
        """
        Generates the Auth Token
        :return: string

        See https://realpython.com/token-based-authentication-with-flask
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=0, minutes=10),
                'iat': datetime.datetime.utcnow(),
                'sub': str(user_id)
            }
            return jwt.encode(
                payload,
                SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            print(__name__, 38, e)
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: user id

        See https://realpython.com/token-based-authentication-with-flask
        """
        try:
            payload = jwt.decode(auth_token, SECRET_KEY)
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Error: Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Error: Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Error: Invalid token. Please log in again.'

    @staticmethod
    def get_user_by_id(id):
        return User.objects(id=id).first()
