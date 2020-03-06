from flask import jsonify

from flask_login import UserMixin
from app import login_manager

from mongoengine.document import Document
from mongoengine.fields import (
  StringField,
  BooleanField
)

from werkzeug.security import check_password_hash

class User(Document, UserMixin):
  meta = {"collection": "Users"}
  email = StringField(required=True, unique=True)
  password_hash = StringField(required=True)
  isAgreeToCollectData = BooleanField(required=True)

  @property
  def is_authenticated(self):
    return True

  @property
  def is_active(self):
      return True

  @property
  def is_anonymous(self):
      return False

  def get_id(self):
      return self.email

  def check_password(self, password):
    """Check hashed password."""
    return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def get_user(email):
  user = User.objects(email=email).first()
  return user

@login_manager.unauthorized_handler
def unauthorized_callback():
  return jsonify({"text": "Logged out."}), 200