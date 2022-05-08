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

@app.route('/')
def index():
    # Verifica que esté loggeado
    if 'user' not in session:
        return redirect(url_for('schedule'))

@app.route('/schedule')
def schedule():
    employees = ([
        Employee('Botero', 'Alejandro Botero'),
        Employee('Pabon', 'Favio Pabón'),
        Employee('Castro', 'Jairo Castro')
    ])
    schedule = Schedule(2022, 6, employees)

    schedule.add_shift(Shift('Botero', 2, 'qx_am'))
    schedule.add_shift(Shift('Pabon', 3, 'n'))
    schedule.add_shift(Shift('Castro', 4, 'ce_pm'))
    schedule.add_shift(Shift('Botero', 5, 'qx_pm'))
    schedule.add_shift(Shift('Castro', 5, 'qx_pm'))

    tmp = '123456789'

    return render_template('schedule.html',
                            tmp=tmp,
                            dow=dow,
                            shifts=Shift.shifts,
                            shift_hours=Shift.shift_hours,
                            schedule=schedule)
