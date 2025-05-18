import os
import secrets
from flask_mail import Message
from Investigation import mail
from PIL import Image
from flask import url_for, current_app

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

def save_picture(image):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(image.filename)
    filename = random_hex + f_ext
    file_path = os.path.join(current_app.root_path, 'static/profile_pics', filename)

    img = Image.open(image)
    i = (125, 125)
    img.thumbnail(i)
    img.save(file_path)

    return filename


t = [(x, y, z) for x in range(2, 4) for y in range(2, 5) for z in range(5, 7) if 2*x*y > 3*z]
