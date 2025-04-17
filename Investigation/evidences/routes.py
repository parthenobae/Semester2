from flask import Blueprint, render_template, redirect, url_for
from Investigation import db
from flask_login import login_required, current_user
from Investigation.models import Case, EvidencePic, EvidenceVid, EvidenceVoice, CaseTeam
from Investigation.evidences.forms import UploadEvidencePics, UploadEvidenceVids
from Investigation.evidences.utils import save_picture, save_video

evidences = Blueprint('evidences', __name__)

@evidences.route('/cases/<int:team_id>', methods=['POST', 'GET'])
@login_required
def cases(team_id):
    casess=Case.query.join(CaseTeam).filter(CaseTeam.team_id==team_id).all()
    return render_template('cases.html', casess=casess, team_id=team_id)

@evidences.route('/case/<int:team_id>/<int:case_id>', methods=['POST', 'GET'])
@login_required
def casee(case_id, team_id):
    casee=Case.query.get(case_id)
    pics=EvidencePic.query.join(Case).filter(Case.id==case_id).all()
    videos=EvidenceVid.query.join(Case).filter(Case.id==case_id).all()
    voices=EvidenceVoice.query.join(Case).filter(Case.id==case_id).all()
    return render_template('case.html', pics=pics, videos=videos, voices=voices, casee=casee, case_id=case_id, team_id=team_id)




@evidences.route('/case/<int:team_id>/<int:case_id>/uploadpic', methods=['POST', 'GET'])
@login_required
def upload_pic(case_id, team_id):
    form = UploadEvidencePics()
    if form.validate_on_submit():
        image_filee = save_picture(form.imagefile.data, team_id, case_id)
        uploadd = EvidencePic(case_id=case_id, image_file=image_filee, 
                              upload_date=form.upload_date.data, uploaded_by=current_user.username, 
                              description=form.description.data)
        db.session.add(uploadd)
        db.session.commit()
        return redirect(url_for('evidences.casee', case_id=case_id, team_id=team_id))
    return render_template('pics.html', form=form)




@evidences.route('/case/<int:team_id>/<int:case_id>/uploadvid', methods=['POST', 'GET'])
@login_required
def upload_vid(case_id, team_id):
    form = UploadEvidenceVids()
    if form.validate_on_submit():
        video_filee = save_video(form.videofile.data, team_id, case_id)
        uploadd = EvidenceVid(case_id=case_id, video_file=video_filee, 
                              upload_date=form.upload_date.data, uploaded_by=current_user.username, 
                              description=form.description.data)
        db.session.add(uploadd)
        db.session.commit()
        return redirect(url_for('evidences.casee', case_id=case_id, team_id=team_id))
    return render_template('vids.html', form=form)
