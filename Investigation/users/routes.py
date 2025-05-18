from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from Investigation.users.forms import RegisterationForm, LoginForm, RequestResetForm, ResetPasswordForm, UpdateForm, AddMembers, AddTeam, AddCase
from Investigation import db, bcrypt
from Investigation.models import User, Team, UserTeam, Case, CaseTeam
from flask_login import current_user, login_user, logout_user, login_required
from Investigation.users.utils import send_reset_email, save_picture


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

@users.route('/account', methods=['POST','GET'])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            current_user.image_file = save_picture(form.picture.data)
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', image_file=image_file,
                            form=form, title="Account")        

@users.route('/manage_teams', methods=['POST', 'GET'])
@login_required
def manage_teams():
    users = User.query.all()
    teams = Team.query.all()
    form = AddTeam()
    if form.validate_on_submit():
        team = Team(name=form.team_name.data)
        db.session.add(team)
        db.session.commit()
        return render_template('manage_teams.html', users=users, teams=teams, form=form)
    return render_template('manage_teams.html', users=users, teams=teams, form=form)

@users.route('/team_details/<int:team_id>', methods=['POST', 'GET'])
@login_required
def team_details(team_id):
    team = Team.query.get_or_404(team_id)
    form = AddMembers()
    form1 = AddCase()
    
    # Get current team members and cases
    users = User.query.join(UserTeam).filter(UserTeam.team_id==team_id).all()
    cases = Case.query.join(CaseTeam).filter(CaseTeam.team_id==team_id).all()
    
    try:
        if form.validate_on_submit():
            # Add member to team
            user_team = UserTeam(user_id=form.userid.data, team_id=team_id)
            db.session.add(user_team)
            db.session.commit()
            flash('Member added successfully', 'success')
            return redirect(url_for('users.team_details', team_id=team_id))
            
        elif form1.validate_on_submit():
            # Add case to team
            case = Case(
                name=form1.case_name.data,
                description=form1.description.data,
                report_date=form1.report_date.data,
                status=form1.status.data,
                location=form1.location.data
            )
            db.session.add(case)
            db.session.flush()  # Assigns ID without committing
            
            case_team = CaseTeam(team_id=team_id, case_id=case.id)
            db.session.add(case_team)
            db.session.commit()
            
            flash('Case added successfully', 'success')
            return redirect(url_for('users.team_details', team_id=team_id))
            
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred: {str(e)}', 'danger')
        current_app.logger.error(f"Team details error: {str(e)}")
    
    return render_template('team_details.html',
                         team=team,
                         form=form,
                         form1=form1,
                         users=users,
                         cases=cases)

@users.route('/delete_user/<int:team_id>/<int:user_id>', methods=['POST', 'GET'])
@login_required
def delete_user(user_id, team_id):
    userr = UserTeam.query.filter_by(user_id=user_id, team_id=team_id).first()
    db.session.delete(userr)
    db.session.commit()
    return redirect(url_for('users.team_details', team_id=team_id))

