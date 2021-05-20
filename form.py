from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

# login form class
class LoginForm(FlaskForm):
    EmpID = StringField("EmpID", validators=[DataRequired()])
    Password = PasswordField("Password", validators=[DataRequired()])
    Submit = SubmitField("Submit")