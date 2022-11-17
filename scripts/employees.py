#!/usr/bin/python3
from os import walk

class Employee:

    def __init__(self, employee):
        self.id, self.name = employee

class Group:
    def __init__(self, id):
        self.id = id
        self.employees = []
        with open(f'user_data/groups/{id}.csv', 'r') as file:
            self.name = file.readline().strip()
            for line in file:
                self.employees += [ Employee(line.strip().split(',')) ]
        self.employees.sort(key=lambda x: x.id)

    def employee_names(self):
        return [ x.name for x in self.employees ]

    def add_employee(self, id, name):
        for e in self.employees:
            if e.id == id:
                raise Exception(f'ID: {id} ya existe en {self.name}')
        self.employees += [ Employee((id, name)) ]
        self.update()

    def rem_employee(self, id):
        self.employees = [ e for e in self.employees if e.id != id ]
        self.update()

    def update(self):
        with open(f'user_data/groups/{self.id}.csv', 'w') as file:
            file.write(f'{self.name}\n')
            for e in self.employees:
                file.write(f'{e.id},{e.name}\n')

    def all_groups():
        for (dirpath, dirnames, filenames) in walk(f'user_data/groups'):
            return [ Group(x[:-4]) for x in filenames ]
