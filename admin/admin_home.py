from flask_admin import Admin
from flask_admin.contrib.mongoengine import ModelView


import models


class UserAdminView(ModelView):
    can_create = False


def create_admin(app):
    admin = Admin(app, name='IdéSYS-ERP Admin', template_mode='bootstrap3')
    admin.add_view(ModelView(models.document.Document))
    admin.add_view(UserAdminView(models.user.User))
    admin.add_view(ModelView(models.black_list_token.BlacklistToken))
