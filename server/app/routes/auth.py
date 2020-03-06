from flask import request, jsonify, session

from flask_login import login_user, login_required, logout_user, current_user

from app import app
from app.models.User import User
from app.forms.AuthForms import SignupForm, LoginForm

from werkzeug.security import generate_password_hash

@app.route("/api/users/register", methods=["POST"])
def register():
  signup_form = SignupForm(obj=request.json)
  if signup_form.validate():
    email = signup_form.email.data
    pwd = signup_form.password.data
    isAgree = signup_form.isAgree.data
    existing_user = User.objects(email=email).first()
    if existing_user is None:
      user = User(email=email,
                  password_hash=generate_password_hash(pwd),
                  isAgreeToCollectData=isAgree).save()
      login_user(user)
      return jsonify({"user": getResponseUser(user)}), 200
    else:
      return jsonify({"text": "Duplicated user."}), 409
  else:
    return jsonify({"text": "Validation error."}), 422

@app.route("/api/users/login", methods=["POST"])
def login():
  login_form = LoginForm(obj=request.json)
  if login_form.validate():
    email = login_form.email.data
    pwd = login_form.password.data
    user = User.objects(email=email).first()
    if user and user.check_password(pwd):
      login_user(user)
      return jsonify({"user": getResponseUser(user)}), 200
    else:
      return jsonify({"text": "Invalid email or password"}), 401
  else:
    return jsonify({"text": "Validation error.", "errors": login_form.errors}), 422

@app.route("/api/users/logout", methods=["GET"])
@login_required
def logout():
  logout_user()
  return jsonify({"text": "Log out."}), 200

@app.route("/api/users/current", methods=["GET"])
def current():
  user = {}
  if not current_user.is_anonymous:
    user = current_user
    return jsonify({"user": getResponseUser(user)}), 200
  return jsonify({"user": None}), 200

def getResponseUser(user):
  rUser = {}
  rUser['id'] = str(user.id)
  rUser['email'] = user.email
  rUser['isAgree'] = user.isAgreeToCollectData
  return rUser
