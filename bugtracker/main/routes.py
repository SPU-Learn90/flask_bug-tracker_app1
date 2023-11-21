from flask import Blueprint, render_template, request, redirect, url_for

from bugtracker.models import Bug, Log
from bugtracker.extensions import db

from datetime import datetime 

main = Blueprint('main', __name__)

@main.route('/')
def index():
    logs = Log.query.order_by(Log.date.desc()).all()

    log_dates = []

    for log in logs:
        description = ''

        for bug in log.bugs:
            description += str(bug.description)

        log_dates.append({
            'log_date' : log,
            'description' : description,
        })

    return render_template('index.html', log_dates=log_dates)

@main.route('/create_log', methods=['POST'])
def create_log():
    date = request.form.get('date')

    if not date:
        # Handle the case where date is empty (you can redirect or show an error message)
        return redirect(url_for('main.index'))

    log = Log(date=datetime.strptime(date, '%Y-%m-%d'))

    db.session.add(log)
    db.session.commit()

    return redirect(url_for('main.view', log_id=log.id))

@main.route('/add')
def add():
    bugs = Bug.query.all()

    return render_template('add.html', bugs=bugs, bug=None)

@main.route('/add', methods=['POST'])
def add_post():
    bug_name = request.form.get('bug-name')
    description = request.form.get('description')

    bug_id = request.form.get('bug-id')

    if bug_id:
        bug = Bug.query.get_or_404(bug_id)
        bug.name = bug_name
        bug.description= description

    else:
        new_bug = Bug(
            name=bug_name,
            description=description, 
        )
    
        db.session.add(new_bug)

    db.session.commit()

    return redirect(url_for('main.add'))

@main.route('/delete_bug/<int:bug_id>')
def delete_bug(bug_id):
    bug = Bug.query.get_or_404(bug_id)
    db.session.delete(bug)
    db.session.commit()

    return redirect(url_for('main.add'))

@main.route('/edit_bug/<int:bug_id>')
def edit_bug(bug_id):
    bug = Bug.query.get_or_404(bug_id)
    bugs = Bug.query.all()

    return render_template('add.html', bug=bug, bugs=bugs)
    
@main.route('/view/<int:log_id>')
def view(log_id):
    log = Log.query.get_or_404(log_id)

    bugs = Bug.query.all()

    totals = {
        'descr' : '',
    }

    for bug in log.bugs:
        totals['descr'] += str(bug.description)

    return render_template('view.html', bugs=bugs, log=log, totals=totals)

@main.route('/add_bug_to_log/<int:log_id>', methods=['POST'])
def add_bug_to_log(log_id):
    log = Log.query.get_or_404(log_id)

    selected_bug = request.form.get('bug-select')

    if selected_bug is not None:
        bug = Bug.query.get(int(selected_bug))

        log.bugs.append(bug)
        db.session.commit()

    return redirect(url_for('main.view', log_id=log_id))

@main.route('/remove_bug_from_log/<int:log_id>/<int:bug_id>')
def remove_bug_from_log(log_id, bug_id):
    log = Log.query.get(log_id)
    bug = Bug.query.get(bug_id)

    log.bugs.remove(bug)
    db.session.commit()

    return redirect(url_for('main.view', log_id=log_id))