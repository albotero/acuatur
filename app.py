#!/usr/bin/python3

from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit

from scripts.calendar import dow
from scripts.employees import Group
from scripts.schedule import Schedule, Shift
from scripts.user import User

import os

app = Flask(__name__, instance_relative_config = True)
app.secret_key = 'acuatur'

socketio = SocketIO(app, cors_allowed_origins = '*', async_mode='gevent') #, logger=True, engineio_logger=True)

os.chdir(os.path.dirname(__file__))

def login_user(user, passwd):
    '''Login user to session'''
    user = User(user, passwd)
    if user.status == 'authenticated':
        session['u'] = user.id
        session['p'] = user.data['password']
    return user, passwd

def logged_user():
    '''Retrieves logged user'''
    return User(session.get('u'), session.get('p'), hashed = True)

@app.route('/')
def index():
    # Requires logged user
    user = logged_user()
    if user.status != 'authenticated':
        return redirect(url_for('login'))

    return render_template('index.html',
            user=user,
            groups=Group.all_groups())

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Verifies if user is logged
    user = logged_user()
    if user.status == 'authenticated':
        return redirect(url_for('.index'))

    if request.method == 'POST':
        result = login_user(request.values.get('user'),
                            request.values.get('password'))
        return render_template('login.html', result = result)

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/schedule', methods=['POST'])
def new_schedule():
    # Requires logged user
    user = logged_user()
    if user.status != 'authenticated':
        return redirect(url_for('login'))

    year, month = [ int(x) for x in request.values.get('month').split('-') ]

    sched = Schedule(
        year,
        month,
        Group(request.values.get('group')),
        user)

    return redirect(url_for('.schedule', filename=sched.id))

@app.route('/schedule/<filename>')
def schedule(filename):
    # Requires logged user
    user = logged_user()
    if user.status != 'authenticated':
        return redirect(url_for('login'))

    if os.path.exists(f'user_data/schedules/{filename}'):
        # Load schedule
        sched = Schedule.load_from_file(filename)
    else:
        # Create new schedule and redirect to the new schedule
        return redirect(url_for('.new_schedule'))

    employees = sched.employees
    empl = {}
    for e in employees:
        empl[e.id] = e.name

    return render_template('schedule.html',
                            dow=dow,
                            shifts=Shift.shifts,
                            shift_hours=Shift.shift_hours,
                            schedule=sched,
                            employees=empl,
                            user=user,
                            groups=Group.all_groups())

@socketio.on('update_schedule')
def update_schedule(data):
    try:
        # Load existing data
        filename = data.get('schedule_id')
        sched = Schedule.load_from_file(filename)

        res = {}

        if data.get('rem'):
            sched.rem_shift(data['rem'])

        if data.get('add'):
            res['add'] = sched.add_shift(
                        data['add']['employee_id'],
                        data['add']['day'],
                        data['add']['shift'],
                        hours = data['add']['hours']
                        )

        # Update schedule
        sched.save_to_file(filename)

        res['result'] = 'ok'
        res['summary'] = sched.summary_html()
        res['cext'] = sched.summary_cext()
        res['extra'] = sched.summary_extra()

        emit('response', res)
    except Exception as ex:
        emit('response', f'error >> {ex}')

@app.route('/del-schedule', methods=['POST'])
def del_schedule():
    Schedule.load_from_file(request.values.get('id')).delete()
    return redirect(url_for('.index'))

@app.route('/password', methods=['GET', 'POST'])
def password():
    # Requires logged user
    user = logged_user()
    if user.status != 'authenticated':
        return redirect(url_for('login'))

    # Updates password
    if request.method == 'POST':
        res = user.update_password(request.values['old_password'], request.values['new_password'])
        return render_template('password.html', user = user, result = res)

    return render_template('password.html', user = user)

@app.route('/dashboard')
def dashboard():
    # Requires admin user
    user = logged_user()
    all_users = User.all_users()
    if request.args.get('u') == 'abotero' and len(all_users) == 0:
        pass
    else:
        if user.status != 'authenticated' or 'admin' not in user.data['roles']:
            return redirect(url_for('login'))

    return render_template('dashboard.html',
                            user = user,
                            groups=Group.all_groups(),
                            all_users=all_users)

@socketio.on('admin')
def admin(data):
    try:
        # Load existing data
        res = {}

        if data.get('add_user'):
            User.create_user(data['add_user'])

        if data.get('rem_user'):
            User.delete_user(data['rem_user'])

        emit('response', {'result': 'ok'})
    except Exception as ex:
        emit('response', f'error >> {ex}')
