from flask import Blueprint, render_template, redirect, url_for, flash, request
from Investigation.users.forms import RegisterationForm, LoginForm, RequestResetForm, ResetPasswordForm
from Investigation import db, bcrypt
from Investigation.models import User, Team, UserTeam
from flask_login import current_user, login_user, logout_user, login_required
from Investigation.users.utils import send_reset_email


users = Blueprint('users', __name__)

@users.route("/register", methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegisterationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash('You have been successfulyy registered, you now login!')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form, title='Register')


@users.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have been successfulyy Signed in', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Cant Login, check your email and password', 'danger')
    return render_template('login.html', form=form, title='Login')

@users.route('/logout',  methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route('/teams',  methods=['POST', 'GET'])
@login_required
def teams():
    teamss = Team.query.join(UserTeam).filter(UserTeam.user_id==current_user.id).all()
    return render_template('teams.html', teamss=teamss)

@users.route('/reset_password',  methods=['POST', 'GET'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Email has been sent with instruction', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title="Request Reset", form=form)

@users.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_token(token)
    if user is None:
        flash('Invalid or expired token', 'warning')
        return redirect('reset_request')
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been Updated, You can now login', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title="Reset Password", form=form)

