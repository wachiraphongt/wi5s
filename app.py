# app.py
"""5s System"""

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
import random

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_manager, login_required, UserMixin, login_user, logout_user, current_user

from form import LoginForm


app = Flask(__name__)

# pip install flask-sqlalchemy
# config sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# login manager for flask-login
login_manager = LoginManager()
login_manager.init_app(app)

# hard coded secret key for development only
app.config['SECRET_KEY'] = 'W8a9c6h2i'

# database table
class ProjectList(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.Text, nullable=False)
    Owner = db.Column(db.Text, nullable=False)

class LocationList(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Location = db.Column(db.Text, nullable=False)

class Log(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Action = db.Column(db.Text, nullable=False)
    Person = db.Column(db.Text, nullable=False)
    Add_Date = db.Column(db.DateTime, default=datetime.utcnow)

class User(UserMixin, db.Model):
    """ Create column to store out data """

    EmpID = db.Column(db.Integer, primary_key=True)
    Password = db.Column(db.Text, nullable=False)
    Name = db.Column(db.Text, nullable=False)
    Role = db.Column(db.Integer, nullable=False)
    ResetPass = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<User {self.id}>"

    def __init__(self, EmpID, Password, Name, Role, ResetPass):
        self.EmpID = EmpID
        self.Password = Password
        self.Name = Name
        self.Role = Role
        self.ResetPass = ResetPass
    
    def verify_password(self, pwd):
        return check_password_hash(self.Password, pwd)

class PartRecord(db.Model):
    """" Create this part record table to store the detail of part """

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PartName = db.Column(db.Text, nullable=False)
    Model = db.Column(db.Text, nullable=False)
    Location = db.Column(db.Integer, db.ForeignKey('location_list.ID'), nullable=False)
    # create foreign key
    location_list = db.relationship(
        'LocationList', backref=db.backref('posts', lazy=True)
    )
    Project = db.Column(db.Integer, db.ForeignKey('project_list.ID'), nullable=False)
    # create foreign key
    project_list = db.relationship(
        'ProjectList', backref=db.backref('posts', lazy=True)
    )
    Quantity = db.Column(db.Integer, nullable=False)
    IsSpared = db.Column(db.Boolean, nullable=False)

@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))

@app.route('/')
def home():
    return render_template('index-new.html')

@app.route('/partcheck/')
def part_check():
    return render_template('partcheck-new.html')

@app.route('/partregis/')
@login_required
def part_register():
    return render_template('partregis-new.html')

@app.route('/partuse/')
def part_use():
    return render_template('partuse-new.html')

@app.route('/sign-up/', methods=["GET", "POST"])
def sign_up():
    """ sign up user account """

    return render_template('sign-up.html')

@app.route('/reset-pwd/')
def reset_pwd():
    """ page to reset password """

    return render_template('reset-pwd.html')

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for(login))

@app.route('/login/', methods=["GET", "POST"])
def login():
    # Create an object called "form" to use LoginForm class
    form = LoginForm()

    EmpID = form.EmpID.data
    Password = form.Password.data

    print(f"{EmpID}\n{Password}")

    # Validate a form submitted by user
    if form.validate_on_submit():
        # Query a user's username from the database
        emp = User.query.filter_by(EmpID=EmpID).first()

        # Check and compare a user's password
        # in a database, if True, log a user in
        if emp and emp.verify_password(Password=Password):
            # Log a user in after completing verifying a password
            # then flash a message "Successful Login"
            login_user(emp)
            
            flash("Successful Login", "success")

            # redirect to homepage
            return redirect(url_for(home))
        else:
            # show flash message "invalid login" if login gets False
            flash("Invalid Login", "danger")

    else:
        # you can print or return something such as an error message
        # In this case, do nothing. But you can do it later
        print("Not")

    return render_template("login.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)