from flask import request, jsonify

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import login_user, login_required, logout_user, current_user

from app import app
from app.models.User import User

@app.route('/api/users/register', methods=['GET', 'POST'])
def register():
  email = request.form['email']
  pwd = request.form['password']
  if request.method == 'POST':
    if email and pwd:
      existing_user = User.objects(email=email).first()
      if existing_user is None:
        hashpass = generate_password_hash(pwd, method='sha256')
        hey = User(email=email, password_hash=hashpass).save()
        login_user(hey)
        return jsonify({'answer': 'Ok!'})
  return jsonify({'answer': 'Not ok!'})