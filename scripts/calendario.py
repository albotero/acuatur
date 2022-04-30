#!/usr/bin/python3

import datetime
from dateutil.easter import easter

dow = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']

def leap_year(year):
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    if year % 4 == 0:
        return True
    return False

def days_in_month(year, month):
    if month in {1, 3, 5, 7, 8, 10, 12}:
        return 31
    if month == 2:
        return 29 if leap_year(year) else 28
    return 30

def next_monday(year, month, day):
    date = datetime.date(year, month, day)
    days = (0 - date.weekday() + 7) % 7 # 0 porque necesitamos el lunes
    return date + datetime.timedelta(days=days)

def festivos(year, month):
    '''Calcula los festivos del año, y los devuelve solo si son del mes'''
    festivos = []

    ### Fecha fija ###
    festivos.append(datetime.date(year, 1, 1)) # Año nuevo
    festivos.append(datetime.date(year, 5, 1)) # Día del trabajo
    festivos.append(datetime.date(year, 7, 20)) # Día de la independencia
    festivos.append(datetime.date(year, 8, 7)) # Batalla de Boyacá
    festivos.append(datetime.date(year, 12, 8)) # Inmaculada concepción
    festivos.append(datetime.date(year, 12, 25)) # Navidad

    ### Trasladable a lunes ###
    festivos.append(next_monday(year, 1, 6)) # Epifanía
    festivos.append(next_monday(year, 3, 19)) # Día de San José
    festivos.append(next_monday(year, 6, 29)) # San Pedro y San Pablo
    festivos.append(next_monday(year, 8, 15)) # Asunción de la virgen
    festivos.append(next_monday(year, 10, 12)) # Día de la raza
    festivos.append(next_monday(year, 11, 1)) # Todos los santos
    festivos.append(next_monday(year, 11, 11)) # Independencia de Cartagena

    ### Según pascua ###
    pascua = easter(year)
    festivos.append(pascua + datetime.timedelta(days=-3)) # Jueves Santo
    festivos.append(pascua + datetime.timedelta(days=-2)) # Viernes Santo
    festivos.append(pascua + datetime.timedelta(days=43)) # Ascensión
    festivos.append(pascua + datetime.timedelta(days=64)) # Corpus Christi
    festivos.append(pascua + datetime.timedelta(days=71)) # Sagrado Corazón de Jesús

    # Devuelve solo los días del mes requerido
    return [x.day for x in festivos if x.month == month]

class Mes:
    def __init__(self, year, month):
        self.titulo = 'Mayo 2022'
        self.dias = days_in_month(year, month)
        self.dia1 = datetime.date(year, month, 1).weekday()
        self.festivos = festivos(year, month)

    def data(self):
        return {
            'titulo': self.titulo,
            'dias': self.dias,
            'dia1': self.dia1,
            'festivos': self.festivos
        }
