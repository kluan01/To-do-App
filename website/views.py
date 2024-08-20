from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required 
def home(): # Runs whenever we type in '/'

    # Creating notes
    if request.method == 'POST':
        note = request.form.get('note')
        due = request.form.get('due')
        subject = request.form.get('subject')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            try:
                due_date = datetime.strptime(due, '%Y-%m-%d') if due else None
                new_note = Note(data=note, user_id=current_user.id, due=due_date, subject=subject)
                db.session.add(new_note)
                db.session.commit()
                flash('Note added!', category='success')

            except ValueError:
                flash('Invalid due date format. Please use YYYY-MM-DD.', category='error')


    return render_template("home.html", user=current_user) # Allows reference to current user

# Turns requested data from JS function to json object to access, find, and delete note ID
@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note: # Quick security check
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
