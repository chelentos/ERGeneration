from flask_login import UserMixin
from app import login_manager

from mongoengine.document import Document
from mongoengine.fields import (
  StringField
)

class User(Document, UserMixin):
  meta = {'collection': 'Users'}
  email = StringField(required=True, unique=True)
  password_hash = StringField(required=True)

@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()