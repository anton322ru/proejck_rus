from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length

class RegisterForm_user(FlaskForm):
    nickname = StringField('Никнейм', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = StringField('Пароль', validators=[DataRequired(), Length(min=6)])
    password_again = StringField('Повторите пароль',
                                  validators=[DataRequired(), EqualTo('password')])
    avatar = FileField('Аватар', validators=[FileAllowed(['jpg', 'png'], 'Только изображения')])


class LoginForm_user(FlaskForm):
    nickname = StringField('Никнейм', validators=[DataRequired()])
    password = StringField('Пароль', validators=[DataRequired()])