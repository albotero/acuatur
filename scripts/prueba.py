from objetos import *

empl1 = Empleado('Alejandro Botero', 2022, 5)
empl1.agregar_turno(1, 'd', 7, 12)
empl1.agregar_turno(2, 'n', 19, 12)
empl1.agregar_turno(3, 'am', 7, 6)
empl1.agregar_turno(4, 'pm', 13, 6)
empl1.agregar_turno(4, 'n', 19, 12)

empl2 = Empleado('Favio Pabon', 2022, 5)
empl2.agregar_turno(1, 'pm', 13, 6)
empl2.agregar_turno(3, 'd', 7, 12)
empl2.agregar_turno(3, 'n', 19, 12)

empl3 = Empleado('Soraya Mera', 2022, 5)
empl3.agregar_turno(2, 'coex', 13, 6)
empl3.agregar_turno(2, 'cenizo', 19, 4)

print(str(empl1))
print(str(empl2))
print(str(empl3))
print()

empl1.borrar_turno(3, 'am')

print(str(empl1))
print(str(empl2))
print(str(empl3))
print()
