#!/usr/bin/python3

from scripts.calendar import Month
from scripts.user import User
import uuid
import os
import pickle

class Shift:

    shift_hours = {
        'am': 6,
        'pm': 6,
        'n': 12
    }

    shifts = {
        'qx_am': 'Quirófano Am',
        'ud_am': 'U.Digestiva Am',
        'ce_am': 'C.Externa Am',
        'qx_pm': 'Quirófano Pm',
        'ud_pm': 'U.Digestiva Pm',
        'ce_pm': 'C.Externa Pm',
        'n': 'Noche',
        'ex': 'Extra'
    }

    def __init__(self, employee_id, day, shift, hours=0, id=None):
        self.employee_id = employee_id
        self.day = day
        self.shift = shift
        self.hours = self.get_shift_hours(shift, hours)
        self.id = uuid.uuid4().hex


    def get_shift_hours(self, shift, hours):
        if hours:
            return hours
        if '_' in shift:
            return self.shift_hours[shift[-2:]]
        return self.shift_hours.get(shift, 0)


class Schedule:

    def __init__(self, year, month, group, user):
        self.year = year
        self.month = month
        self.group = group
        self.user = user
        self.employees = group.employees
        self.shifts = []

        self.id = uuid.uuid4().hex
        self.save_to_file(self.id)

        self.user.data['schedules'] = f"{self.user.data['schedules']}|" if self.user.data.get('schedules') else ''
        self.user.data['schedules'] += f"{self.year}-{self.month:02d}@{self.get_month().title}@{group.name}@{self.id}"
        self.user.save_data()

    def get_month(self):
        return Month(self.year, self.month)

    def add_shift(self, employee_id, day, shift, hours = 0):
        s = Shift(employee_id, day, shift, hours = hours)
        self.shifts.append(s)
        return {
            'id': s.id,
            'employee_id': s.employee_id,
            'hours': s.hours,
            'day': day,
            'shift': shift
            }

    def rem_shift(self, shift_id):
        self.shifts = [x for x in self.shifts if x.id != shift_id]

    def employees_in_day(self, day):
        res = {}
        for shift in Shift.shifts.keys():
            res[shift] = []
        for shift in [x for x in self.shifts if x.day == day]:
            res[shift.shift].append((shift.id, shift.employee_id, shift.hours))
        return res

    def employee_hours(self, employee_id = None, shift = None, holidays = None):
        return sum([ x.hours for x in self.shifts if (
                            (x.employee_id == employee_id if employee_id else True) and
                            (shift in x.shift if shift else True) and
                            (self.get_month().sunday_or_holiday(x.day)
                                if holidays
                                else (not self.get_month().sunday_or_holiday(x.day))
                                    if holidays == False
                                    else True)
                            ) ])

    def summary(self):
        titles = ['anestesiólogo', 'total horas', 'noche',
                    'fest-dom día', 'día', 'c. externa',
                    'u. digestiva', 'horas extra']
        summary = []

        for e in self.employees:
            # Employee names
            row = [e.id]

            # Total hours
            row += [self.employee_hours(employee_id = e.id)]

            # Night shifts
            row += [self.employee_hours(employee_id = e.id, shift = 'n')]

            # Holiday-Sunday day shifts
            holiday_sunday = (
                self.employee_hours(employee_id = e.id, shift = 'qx_am', holidays = True) +
                self.employee_hours(employee_id = e.id, shift = 'qx_pm', holidays = True)
                )
            row += [ holiday_sunday ]

            # Day shifts
            row += [
                self.employee_hours(employee_id = e.id, shift = 'qx_am')
                + self.employee_hours(employee_id = e.id, shift = 'qx_pm')
                - holiday_sunday
                ]

            # C.E. shifts
            row += [
                self.employee_hours(employee_id = e.id, shift = 'ce_am')
                + self.employee_hours(employee_id = e.id, shift = 'ce_pm')
                ]

            # U.D. shifts
            row += [
                self.employee_hours(employee_id = e.id, shift = 'ud_am')
                + self.employee_hours(employee_id = e.id, shift = 'ud_pm')
                ]

            # Extra hours
            row += [self.employee_hours(employee_id = e.id, shift = 'ex')]

            summary.append(row)

        # Row of totals
        totals = [ 'Total' ]
        for i in range(1, len(summary[0])):
            totals += [ sum([ summary[x][i] for x in range(len(summary)) ]) ]
        summary.append(totals)

        for a in range(len(summary)):
            summary[a][1] = f'{summary[a][1]} H' # Totales
            summary[a][-1] = f'{summary[a][-1]} H' # Extras
            for b in range(2, len(summary[0]) - 1):
                total_shifts = summary[a][b] / 12
                total_shifts = int(total_shifts) if float(total_shifts).is_integer() else total_shifts
                summary[a][b] = f'{total_shifts}: {summary[a][b]} H'

        return titles, summary

    def summary_html(self):
        sum_titles, sum_rows = self.summary()

        html = '''
            <thead>
              <th colspan="8">Total Horas</th>
            <tr>
            '''
        for title in sum_titles:
            html += f'<th>{title}</th>'
        html += '''
                </tr>
            </thead>
            '''

        for row in sum_rows:
            html += '<tr>'
            for val in row:
                html += f'<td>{val}</td>'
            html += '</tr>'

        return html

    def summary_cext(self):
        '''Returns list of tuples with day, employee, shift, hours in cext'''
        cext = []
        for shift in self.shifts:
            if 'ce' in shift.shift:
                cext.append( (shift.day,
                              f'{shift.day}/{self.month}/{self.year}',
                              shift.employee_id,
                              shift.shift[-2:],
                              shift.hours) )
        cext.sort(key=lambda x: x[0])

        if not len(cext):
            return ''

        html = '''
            <thead>
              <th colspan="4">Consulta Externa</th>
              <tr>
                  <th>D&iacute;a</th>
                  <th>Anestesi&oacute;logo</th>
                  <th>Horario</th>
                  <th>Horas</th>
              </tr>
            </thead>
            '''
        for ce_day, ce_date, ce_employee, ce_shift, ce_hours in cext:
            html += f'''
                <tr>
                  <td>{ce_date}</td>
                  <td>{ce_employee}</td>
                  <td>{ce_shift}</td>
                  <td>{ce_hours} horas</td>
                </tr>
                '''
        return html

    def summary_extra(self):
        '''Returns list of tuples with day, employee, shift, hours in extra'''
        extra = []
        for shift in self.shifts:
            if 'ex' in shift.shift:
                extra.append( (shift.day,
                              f'{shift.day}/{self.month}/{self.year}',
                              [x.name for x in self.group.employees if x.id == shift.employee_id][0],
                              shift.hours) )
        extra.sort(key=lambda x: x[0])

        if not len(extra):
            return ''

        html = '''
            <thead>
              <th colspan="3">Horas Extra</th>
              <tr>
                  <th>D&iacute;a</th>
                  <th>Anestesi&oacute;logo</th>
                  <th>Horas</th>
              </tr>
            </thead>
            '''
        for ex_day, ex_date, ex_employee, ex_hours in extra:
            html += f'''
                <tr>
                  <td>{ex_date}</td>
                  <td>{ex_employee}</td>
                  <td>{ex_hours} horas</td>
                </tr>
                '''
        return html

    def save_to_file(self, filename):
        '''Serializes all schedule and saves it to a file'''
        # Open a file and use dump()
        with open(f'user_data/schedules/{filename}', 'wb') as file:
            pickle.dump(self, file)

    def load_from_file(filename):
        '''Loads a serialized schedule from a file'''
        # Open the file in binary mode
        with open(f'user_data/schedules/{filename}', 'rb') as file:
            # Call load method to deserialze
            return pickle.load(file)

    def delete(self):
        # Update user data
        self.user.load_data()
        # Remove schedule from user
        self.user.data['schedules'] = '|'.join([ x for x in self.user.data.get('schedules', []).split('|')
                                                    if self.id not in x ])
        # Save user data
        self.user.save_data()
        # Delete schedule from files
        os.remove(f'user_data/schedules/{self.id}')
