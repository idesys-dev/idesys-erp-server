import datetime


import mongoengine as me


class BlacklistToken(me.Document):
    token = me.StringField(required=True)
    blacklisted_on = me.DateTimeField()

    @staticmethod
    def new_black_list_token(token):
        black_list_token = BlacklistToken(token=token, blacklisted_on=datetime.datetime.now())
        black_list_token.save()

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.objects(token=str(auth_token))
        if res:
            return True
        else:
            return False
