from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired


class RegisterForm_job(FlaskForm):
    team_leader = IntegerField('Team Leader id', validators=[DataRequired()])
    job = StringField('Job Title', validators=[DataRequired()])
    work_size = IntegerField('Work Size', validators=[DataRequired()])
    collaborators = StringField('Collaborators', validators=[DataRequired()])
    is_finished = BooleanField('Is Job finished?')
    submit = SubmitField('Submit')
