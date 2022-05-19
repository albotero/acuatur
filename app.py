#!/usr/bin/python3

from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit

from scripts.calendar import dow
from scripts.schedule import Schedule, Shift

import os

app = Flask(__name__, instance_relative_config = True)
app.secret_key = 'acuatur'

socketio = SocketIO(app, cors_allowed_origins = '*', async_mode='gevent') #, logger=True, engineio_logger=True)

os.chdir(os.path.dirname(__file__))

@app.route('/')
def index():
    # Verifica que esté loggeado
    if 'user' not in session:
        return redirect(url_for('schedule'))

@app.route('/schedule')
def new_schedule():
    employees = ([
        ('naranjo', 'Naranjo'),
        ('bolaños', 'Jaime Bolaños'),
        ('cardona', 'Eduin Cardona'),
        ('pabon', 'Favio Pabón'),
        ('mera', 'Soraya Mera'),
        ('m. orozco', 'Mario Orozco'),
        ('posso', 'Mónica Posso'),
        ('arroyave', 'Julián Arroyave'),
        ('vallejos', 'Lorena Vallejos'),
        ('benjumea', 'Angélica Benjumea'),
        ('morales', 'Maryurin Morales'),
        ('serna', 'Ana Milena Serna'),
        ('rosillo', 'Andrés Rosillo'),
        ('gallego', 'Gallego'),
        ('alvarez', 'Danik Álvarez'),
        ('castro', 'Jairo Castro'),
        ('botero', 'Alejandro Botero'),
        ('jf. orozco', 'Johann Orozco'),
        ('vaisman', 'Vaisman'),
        ('pardo', 'Hernán Pardo')
    ])
    sched = Schedule(2022, 4, employees)
    return redirect(url_for('.schedule', filename=sched.id))

@app.route('/schedule/<filename>')
def schedule(filename):
    if os.path.exists(f'schedules/{filename}'):
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
                            employees=empl)

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

        emit('response', res)
    except Exception as ex:
        emit('response', f'error >> {ex}')
