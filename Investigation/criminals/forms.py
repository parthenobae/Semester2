from flask_wtf import FlaskForm
from Investigation.models import User, Team
from flask_wtf.file import FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, IntegerField
from wtforms.validators import Email, DataRequired, Length, EqualTo, ValidationError


class dna_form(FlaskForm):
    dna_file = FileField('DNA Sequence', validators=[FileAllowed(['txt'])])
    submit = SubmitField('Search')
