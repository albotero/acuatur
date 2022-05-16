#!/usr/bin/python3

from scripts.calendar import Month

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

    def __init__(self, employee_id, day, shift, hours=0):
        self.employee_id = employee_id
        self.day = day
        self.shift = shift
        self.hours = self.get_shift_hours(shift, hours)

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

    def add_shift(self, shift):
        self.shifts.append(shift)

    def rem_shift(self, employee_id, day, shift):
        self.shifts = [x for x in self.shifts if (  x.employee_id != employee_id and
                                                    x.day != day and
                                                    x.shift != shift )]

    def employees_in_day(self, day):
        res = {}
        for shift in Shift.shifts.keys():
            res[shift] = []
        for shift in [x for x in self.shifts if x.day == day]:
            res[shift.shift].append((shift.employee_id, shift.hours))
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
            ## All holliday/sundays (d+n) minus nights
            hs_hours = self.employee_hours(employee_id = e.id, holidays = True)
            hs_nights = self.employee_hours(employee_id = e.id, shift = 'n', holidays = True)
            hs_days = hs_hours - hs_nights
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

        return titles, summary
