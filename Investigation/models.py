from Investigation import db, login_manager
from flask import current_app
from itsdangerous import URLSafeTimedSerializer
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String, default="default.jpg")
    password = db.Column(db.String, nullable=False)
    teams = db.relationship('UserTeam', backref='user', lazy=True)

    def generate_token(self):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id':self.id})
    
    @staticmethod
    def verify_token(token):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=1800)['user_id']
        except Exception:
            return None
        return  User.query.get(user_id)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True, nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    report_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status=db.Column(db.String(30), nullable=False)
    location=db.Column(db.String(30), nullable=False)
    teams = db.relationship('CaseTeam', backref='case', lazy=True)
    evidence_pics=db.relationship('EvidencePic', backref='case', lazy=True)
    evidence_vids=db.relationship('EvidenceVid', backref='case', lazy=True)
    evidence_voices=db.relationship('EvidenceVoice', backref='case', lazy=True)

    def __repr__(self):
        return f"Case('{self.id}', '{self.name}')"
    
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True, nullable=False)
    users = db.relationship('UserTeam', backref='team', lazy=True)
    cases = db.relationship('CaseTeam', backref='team', lazy=True)

    def __repr__(self):
        return f"Team('{self.id}', '{self.name}')"
    
class UserTeam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    __table_args__ = (
        db.UniqueConstraint('user_id', 'team_id', name='unique_user_team'),
    )

class CaseTeam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'), nullable=False)
    __table_args__ = (
        db.UniqueConstraint('team_id', 'case_id', name='unique_team_case'),
    )

class EvidencePic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'), nullable=False)
    image_file=db.Column(db.String, nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    uploaded_by=db.Column(db.String(30),nullable=False)
    description = db.Column(db.String(1000), nullable=False)


class EvidenceVid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'), nullable=False)
    video_file=db.Column(db.String, nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    uploaded_by=db.Column(db.String(30),nullable=False)
    description = db.Column(db.String(1000), nullable=False)
  

class EvidenceVoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'), nullable=False)
    voice_file=db.Column(db.String, nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    uploaded_by=db.Column(db.String(30),nullable=False)
    description = db.Column(db.String(1000), nullable=False)


class Criminals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True, nullable=False)
    image_file=db.Column(db.String, nullable=False)
