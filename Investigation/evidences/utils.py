import secrets
import os
from PIL import Image
from flask import current_app

def save_picture(form_picture, team_id, case_id):
    tok = secrets.token_hex(8)
    _, file_ext=os.path.split(form_picture.filename)
    picture_fn=tok + file_ext
    picture_folder=os.path.join(current_app.root_path, 'static','evidence', 'pics', str(case_id))
    picture_path=os.path.join(picture_folder, picture_fn)

    img = Image.open(form_picture)
    img.thumbnail((1280, 960))
    img.save(picture_path, quality=85)

    return picture_fn

def save_video(form_video, team_id, case_id):
    tok = secrets.token_hex(8)
    _, file_ext=os.path.splitext(form_video.filename)
    video_fn=tok + file_ext
    video_folder=os.path.join(current_app.root_path, 'static','evidence', 'videos', str(case_id))
    video_path=os.path.join(video_folder, video_fn)

    form_video.save(video_path)

    return video_fn