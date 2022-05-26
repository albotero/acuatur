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

    def employee_names(self):
        return [ x.name for x in self.employees ]

    def all_groups():
        for (dirpath, dirnames, filenames) in walk(f'user_data/groups'):
            return [ Group(x[:-4]) for x in filenames ]
