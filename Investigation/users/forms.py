from flask_wtf import FlaskForm
from Investigation.models import User, Team, Case
from flask_wtf.file import FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, IntegerField, DateField, TextAreaField
from wtforms.validators import Email, DataRequired, Length, EqualTo, ValidationError

class RegisterationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
        

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    remember = BooleanField('Remember Me')


class UpdateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=10)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Profile Pic', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')
        
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('You are not registered, register yourself first!')
    
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class AddMembers(FlaskForm):
    userid = IntegerField('User Id', validators=[DataRequired()])
    submit = SubmitField('Add User')

    def validate_userid(self, userid):
        user = User.query.get(userid.data)
        if user is None:
            raise ValidationError('This officer is not found')
        
class AddTeam(FlaskForm):
    team_name = StringField('Team Name', validators=[DataRequired()])
    submit = SubmitField('Add Team')

    def validate_team_name(self, team_name):
        team = Team.query.filter_by(name=team_name.data).first()
        if team:
            raise ValidationError('This name is already taken, choose a different one!')

class AddCase(FlaskForm):
    case_name = StringField('Case Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    report_date = DateField('Case Name', validators=[DataRequired()])
    status = StringField('Status', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Add Case')

    def validate_case_name(self, case_name):
        case = Case.query.filter_by(name=case_name.data).first()
        if case:
            raise ValidationError('This case is going on, choose a different one!')
        
