#!/usr/bin/python3

import datetime
from dateutil.easter import easter

dow = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']

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

def holidays(year, month):
    '''Returns holidays in the required month'''
    holidays = []

    ### Fecha fija ###
    holidays.append(datetime.date(year, 1, 1)) # Año nuevo
    holidays.append(datetime.date(year, 5, 1)) # Día del trabajo
    holidays.append(datetime.date(year, 7, 20)) # Día de la independencia
    holidays.append(datetime.date(year, 8, 7)) # Batalla de Boyacá
    holidays.append(datetime.date(year, 12, 8)) # Inmaculada concepción
    holidays.append(datetime.date(year, 12, 25)) # Navidad

    ### Trasladable a lunes ###
    holidays.append(next_monday(year, 1, 6)) # Epifanía
    holidays.append(next_monday(year, 3, 19)) # Día de San José
    holidays.append(next_monday(year, 6, 29)) # San Pedro y San Pablo
    holidays.append(next_monday(year, 8, 15)) # Asunción de la virgen
    holidays.append(next_monday(year, 10, 12)) # Día de la raza
    holidays.append(next_monday(year, 11, 1)) # Todos los santos
    holidays.append(next_monday(year, 11, 11)) # Independencia de Cartagena

    ### Según pascua ###
    _easter = easter(year)
    holidays.append(_easter + datetime.timedelta(days=-3)) # Jueves Santo
    holidays.append(_easter + datetime.timedelta(days=-2)) # Viernes Santo
    holidays.append(_easter + datetime.timedelta(days=43)) # Ascensión
    holidays.append(_easter + datetime.timedelta(days=64)) # Corpus Christi
    holidays.append(_easter + datetime.timedelta(days=71)) # Sagrado Corazón de Jesús

    # Devuelve solo los días del mes requerido
    return [x.day for x in holidays if x.month == month]

class Month:
    def __init__(self, year, month):
        self.title = 'Mayo 2022'
        self.days = days_in_month(year, month)
        self.day1 = datetime.date(year, month, 1).weekday()
        self.holidays = holidays(year, month)
