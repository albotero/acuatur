#!/usr/bin/python3

from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit

from scripts.calendario import Mes, dow

import os

app = Flask(__name__, instance_relative_config = True)
app.secret_key = 'acuatur'

socketio = SocketIO(app, cors_allowed_origins = '*', async_mode='gevent') #, logger=True, engineio_logger=True)

os.chdir(os.path.dirname(__file__))

@app.route('/')
def index():
    # Verifica que esté loggeado
    if 'usuario' not in session:
        return redirect(url_for('cuadro'))
    return None

@app.route('/cuadro')
def cuadro():
    tmp = '123456789'

    return render_template('cuadro.html',
                            tmp=tmp,
                            dow=dow,
                            mes=Mes(2022, 5).data())
