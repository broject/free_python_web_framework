from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from app.auth_models import User

class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    email = StringField('И-мэйл', validators=[DataRequired(), Email()])
    password = PasswordField('Нууц үг', validators=[DataRequired()])
    submit = SubmitField('Нэвтрэх')