from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length

class RegisterForm_user(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = StringField('Пароль', validators=[DataRequired(), Length(min=6)])
    password_again = StringField('Повторите пароль',
                                  validators=[DataRequired(), EqualTo('password')])

class LoginForm_user(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = StringField('Пароль', validators=[DataRequired()])