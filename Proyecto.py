#* Rafael Díaz Medina A01024592
from datetime import datetime

# Opening a file
file1 = open('data.txt', 'w')

actionName = input("Cuál es el nombre de la acción: ")
file1.writelines("Precio: "+actionName+"\n")

price = input("Cuál fue el precio de la acción: ")
file1.writelines("Precio: "+price+"\n")

fee = input("Cuál fue la comisión: ")
file1.writelines("Comisión: "+fee+"\n")

dateIf = input("Compraste la acción hoy? ")
if dateIf == "y":
    ndate = datetime.today().strftime('%Y-%m-%d')
    file1.writelines("Fecha de Compra: "+ndate+"\n")
else:
    date = input("Dime la fecha de cuando compraste la acción: ")
    file1.writelines("Fecha de Compra: "+date+"\n")

file1.close()
