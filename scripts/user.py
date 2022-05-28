#!/usr/bin/python3

from datetime import datetime

import hashlib
import os

class Password:
    salt_length = 8

    def hash_password(password, salt = None):
        '''Returns a hashed password'''
        salt = bytes.fromhex(salt) if salt else os.urandom(Password.salt_length)

        key = hashlib.pbkdf2_hmac(
            'sha256', # The hash digest algorithm for HMAC
            password.encode('utf-8'), # Convert the password to bytes
            salt, # Provide the salt
            100000 # It is recommended to use at least 100,000 iterations of SHA-256
        )
        return f'{salt.hex()}{key.hex()}'

    def try_password(password, stored_password, hashed):
        '''Returns true if password matches with stored_password'''
        salt = stored_password[:Password.salt_length * 2]
        password = password if hashed else Password.hash_password(password, salt)
        return password == stored_password

class User:
    def __init__(self, id, passwd, hashed = False):
        self.id = id
        self.path = f'user_data/users/{self.id}.conf'
        self.status = 'created'
        self.passwd = passwd
        self.hashed = hashed

        if not id:
            self.status = 'no_id'
        elif not passwd:
            self.status = 'no_password'
        elif not os.path.exists(self.path):
            self.status = 'wrong_id'
        else:
            self.data = {}
            self.load_data()

    def load_data(self):
        '''Load data into dict'''
        with open(self.path, 'r') as file:
            for line in file:
                data = line.split('\t')
                self.data[data[0].strip()] = data[1].strip()
        if Password.try_password(self.passwd, self.data.get('password'), self.hashed):
            self.status = 'authenticated'
        else:
            self.status = 'wrong_password'

    def save_data(self):
        '''Rewrites all details into conf file'''
        with open(self.path, 'w') as file:
            for key, item in self.data.items():
                file.write(f'{key}\t{item}\n')

    def message(self):
        m = {
            'authenticated': 'Autenticado',
            'created': f'Se creó el usuario <b><i>{self.id}</i></b>',
            'no_id': 'No ha iniciado sesión',
            'no_password': 'No especificó una contraseña',
            'wrong_id': f'El usuario <b><i>{self.id}</i></b> no existe',
            'wrong_password': 'Clave errada'
        }
        return m[self.status]

    def update_password(self, old_pass, new_pass):
        '''If old_pass matches current one, updates it with new_pass'''

        if not Password.try_password(old_pass, self.passwd, hashed = False):
            return 'error', 'Contrase&ntilde;a Actual errada. Por favor intenta nuevamente.'

        if len(new_pass) < 6:
            return 'error', 'La Nueva Contrase&ntilde;a debe tener por lo menos 6 caracteres.'

        # Passwords are ok, updates with new_pass
        salt = self.data['password'][:Password.salt_length * 2]
        self.data['password'] = Password.hash_password(new_pass, salt)
        self.save_data()
        return 'success', 'Se cambi&oacute; la contrase&ntilde;a correctamente.'