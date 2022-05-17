#!/usr/bin/python3

from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit

from scripts.calendar import dow
from scripts.schedule import Employee, Shift, Schedule

import os

app = Flask(__name__, instance_relative_config = True)
app.secret_key = 'acuatur'

socketio = SocketIO(app, cors_allowed_origins = '*', async_mode='gevent') #, logger=True, engineio_logger=True)

os.chdir(os.path.dirname(__file__))


employees = ([
    Employee('naranjo', 'Naranjo'),
    Employee('bolaños', 'Jaime Bolaños'),
    Employee('cardona', 'Eduin Cardona'),
    Employee('pabon', 'Favio Pabón'),
    Employee('mera', 'Soraya Mera'),
    Employee('m. orozco', 'Mario Orozco'),
    Employee('posso', 'Mónica Posso'),
    Employee('arroyave', 'Julián Arroyave'),
    Employee('vallejos', 'Lorena Vallejos'),
    Employee('benjumea', 'Angélica Benjumea'),
    Employee('morales', 'Maryurin Morales'),
    Employee('serna', 'Ana Milena Serna'),
    Employee('rosillo', 'Andrés Rosillo'),
    Employee('gallego', 'Gallego'),
    Employee('alvarez', 'Danik Álvarez'),
    Employee('castro', 'Jairo Castro'),
    Employee('botero', 'Alejandro Botero'),
    Employee('jf. orozco', 'Johann Orozco')
])
employees.sort(key=lambda x: x.id)
sched = Schedule(2022, 4, employees)
tmp = '123456789'


@app.route('/')
def index():
    # Verifica que esté loggeado
    if 'user' not in session:
        return redirect(url_for('schedule'))

@app.route('/schedule')
def schedule():
    empl = {}
    for e in employees:
        empl[e.id] = e.name
    return render_template('schedule.html',
                            tmp=tmp,
                            dow=dow,
                            shifts=Shift.shifts,
                            shift_hours=Shift.shift_hours,
                            schedule=sched,
                            employees = empl)

@socketio.on('update_schedule')
def update_schedule(data):
    try:
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

        res['result'] = 'ok'
        res['summary'] = sched.summary_html()

        emit('response', res)
    except Exception as ex:
        emit('response', f'error >> {ex}')
