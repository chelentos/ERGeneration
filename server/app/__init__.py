from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from pymongo import MongoClient
from flask_session import Session
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from flask_mongoengine import MongoEngine
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import session

from app.config import Config

# configuration
db = MongoEngine()
csrf = CSRFProtect()
login_manager = LoginManager()
cors = CORS(resources={ r'/*': {'origins': '*'}}, supports_credentials=True)

mongo_client = MongoClient("mongodb://er-ad:t100km0201@localhost:27017/er-gen?authSource=er-gen")
sess = Session()

# instantiate the app
app = Flask(__name__)
app.config.from_object(Config)
app.config['SESSION_TYPE'] = 'mongodb'
app.config['SESSION_MONGODB'] = mongo_client
app.config['SESSION_MONGODB_DB'] = 'er-gen'
sess.init_app(app)
db.init_app(app)
cors.init_app(app)
csrf.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.session_protection = "basic"

from .routes import auth, projects
