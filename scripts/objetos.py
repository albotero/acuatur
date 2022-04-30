#!/usr/bin/python3

from datetime import datetime

class Turno:

    def __init__(self, tipo, y, m, dia, hora_inicio, horas):
        '''Crea una nueva instancia de un Turno'''

        if hora_inicio + horas > 23:
            dia = dia + 1
            hora_inicio = hora_inicio + horas - 24

        self.tipo = tipo
        self.dia = dia
        self.hora_inicio = datetime(y, m, dia, hora_inicio, 0, 0)
        self.hora_fin = datetime(y, m, dia, hora_inicio + horas, 0, 0)

    def __str__(self):
        hora_i = self.hora_inicio.strftime("%Y-%m-%d %I:%M:%S %p")
        hora_f = self.hora_fin.strftime("%Y-%m-%d %I:%M:%S %p")
        return f'{self.hora_inicio.strftime("%d")} -> {hora_i} - {hora_f}'

    def horas(self):
        '''Horas de duración del turno'''
        diff = (self.hora_fin - self.hora_inicio).total_seconds()
        return int(diff) // (60*60)


class Empleado:

    def __init__(self, id, nombre, y, m):
        '''Crea una nueva instancia de un empleado'''
        self.id = id
        self.nombre = nombre
        self.y = y
        self.m = m
        self.turnos = []

    def __str__(self):
        horas = self.horas_mes()
        res = f'Empleado: {self.id}'
        for tipo, num_horas in horas.items():
            res += f'\n  {tipo.capitalize()} -> {num_horas} horas'
        return res

    def agregar_turno(self, dia, tipo, hora_inicio = 0, horas = 0):
        '''Agrega un nuevo turno al empleado'''
        self.turnos.append(Turno(tipo, self.y, self.m, dia, hora_inicio, horas))

    def borrar_turno(self, dia, tipo, hora_inicio = 0, horas = 0):
        '''Borra el turno'''
        self.turnos = [i for i in self.turnos if not (i.tipo == tipo and i.dia == dia)]

    def horas_mes(self):
        '''Calcula las horas laboradas en el mes'''
        res = {}

        for turno in self.turnos:
            horas_turno = turno.horas()
            for key in ['total', turno.tipo]:
                res[key] =  res.get(key, 0) + horas_turno

        return res
