from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, current_app
from Investigation.criminals.forms import dna_form
from Investigation import db, bcrypt
from Investigation.models import Criminals
from flask_login import current_user, login_user, logout_user, login_required
from Investigation.criminals.utils import sequence_checker, longest_match
import os
from io import TextIOWrapper

criminals = Blueprint('criminals', __name__)

@criminals.route("/profiling", methods=['POST', 'GET'])
@login_required
def profiling():
    form = dna_form()
    if form.validate_on_submit():
        # Use absolute path or config-based path
        db_path = os.path.join(os.path.dirname(__file__), 'people_data.csv')
        
    try:
        sequence_file = form.dna_file.data
        sq_file = os.path.join(current_app.root_path, 'criminals', 'sequences', sequence_file.filename)
        sequence_file.save(sq_file)
        
        result = sequence_checker(db_path, sq_file)
        if os.path.exists(sq_file):
            os.remove(sq_file)
        
        if result:
            criminal = Criminals.query.filter_by(name=result).first()
            if criminal:
                return redirect(url_for('criminals.account_criminal', 
                                     criminal_id=criminal.id))
            flash('No matching criminal found in database', 'warning')
        else:
            flash('No DNA match found', 'warning')
    except Exception as e:
        flash(f'Error processing files: {str(e)}', 'danger')
            
    return render_template('dna_profiling.html', form=form, title='DNA Profiling')

@criminals.route('/profiling/<int:criminal_id>', methods=['GET'])
@login_required
def account_criminal(criminal_id):
    criminal = Criminals.query.get_or_404(criminal_id)
    return render_template('account_criminal.html', 
                         criminal=criminal, 
                         title="Criminal Profile")

# utils.py would contain the sequence_checker and longest_match functions