import os
from flask_mail import Message
from Investigation import mail
from flask import url_for

def send_reset_email(user):
    token = user.generate_token()
    msg = Message('Password Reset Request', 
                  sender=os.environ.get('EMAIL_USER'),
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_password', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)