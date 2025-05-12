from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_wtf.file import FileField, FileAllowed

class RegisterForm_user(FlaskForm):
    nickname = StringField('Никнейм', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    password_again = PasswordField('Повторите пароль',
                                validators=[DataRequired(), EqualTo('password')])
    avatar = FileField('Аватар', validators=[FileAllowed(['jpg', 'png'], 'Только изображения')])

class LoginForm_user(FlaskForm):
    nickname = StringField('Никнейм', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])