from flask import Flask, render_template, request, redirect, url_for, jsonify

from flask_cors import CORS

from flask_mongoengine import MongoEngine

from flask_login import LoginManager, login_user, login_required, logout_user, current_user

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)

# mongodb
app.config['MONGODB_SETTINGS'] = {
  'db': 'ergeneration',
  'host': 'mongodb://er-ad:t100km0201@localhost:27017/er-gen?authSource=er-gen'
}

# secret key to prevent CSRF
app.config['SECRET_KEY'] = 'mysEcrEtkEy'

db = MongoEngine(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app.routes import auth
