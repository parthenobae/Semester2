from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import Email, DataRequired

class UploadEvidencePics(FlaskForm):
    upload_date=DateField('Upload Date', format='%Y-%m-%d')
    imagefile=FileField('Picture', validators=[FileAllowed(['jpg', 'png'])])
    description=TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Upload')

class UploadEvidenceVids(FlaskForm):
    upload_date=DateField('Upload Date', format='%Y-%m-%d')
    videofile=FileField('Video')
    description=TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Upload')