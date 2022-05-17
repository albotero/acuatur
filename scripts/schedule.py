#!/usr/bin/python3

from scripts.calendar import Month
import uuid

class Employee:

    def __init__(self, id, name):
        self.id = id
        self.name = name


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
        self.id = id if id else uuid.uuid4().hex

    def get_shift_hours(self, shift, hours):
        if hours:
            return hours
        if '_' in shift:
            return self.shift_hours[shift[-2:]]
        return self.shift_hours.get(shift, 0)


class Schedule:

    def __init__(self, year, month, employees):
        self.year = year
        self.month = month
        self.employees = employees
        self.shifts = []

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
                            (self.get_month().sunday_or_holiday(x.day) if holidays else True)
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
            ## All holliday/sundays (d+n) minus nights and extra
            hs_hours = self.employee_hours(employee_id = e.id, holidays = True)
            hs_nights = self.employee_hours(employee_id = e.id, shift = 'n', holidays = True)
            hs_extra = self.employee_hours(employee_id = e.id, shift = 'ex', holidays = True)
            hs_days = hs_hours - hs_nights - hs_extra
            row += [ hs_days ]

            # Day shifts
            row += [
                self.employee_hours(employee_id = e.id, shift = 'qx_am')
                + self.employee_hours(employee_id = e.id, shift = 'qx_pm')
                - hs_days
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

        html = '<tr>'
        for title in sum_titles:
            html += f'<th>{title}</th>'
        html += '</tr>'

        for row in sum_rows:
            html += '<tr>'
            for val in row:
                html += f'<td>{val}</td>'
            html += '</tr>'

        return html
