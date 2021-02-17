# app.py
# WI5S

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
import random

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user, current_user

from form import LoginForm


app = Flask(__name__)

# pip install flask-sqlalchemy
# config sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# login manager for flask login
login_manager = LoginManager()
login_manager.init_app(app)

# hard coded secret key for development only
app.config['SECRET_KEY'] = "iwillcontinue"

class User(UserMixin, db.Model):
    """ Create column to strore out data """

    # id, password, role, register_date
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    role = db.Column(db.Text, nullable=False)
    register_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.id}"

    def __init__(self, id, password, name, role):
        self.id = id
        self.password = password
        self.name = name
        self.role = role

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('home.html', title="Test1")

@app.route('/about')
def about():
	return "About Us"    
