#* Rafael Díaz Medina A01024592

from datetime import datetime

file1 = open('portfolio.txt', 'a')

actionType = input("Qué tipo de producto compraste\n 1* Forward\n 2* Call/Put\n 3* Nota Estructurada\n 4* Buscar Average \n")


def forward():
    file1.writelines("Forward \n")
    actionName = input("Cuál es el nombre de la acción: ")
    file1.writelines("Nombre: "+actionName+"\n")

    price = input("Cuál fue el precio de la acción: ")
    file1.writelines("Precio: "+price+"\n")

    fee = input("Cuál fue la comisión: ")
    file1.writelines("Comisión: "+fee+"\n")

    dateIf = input("Compraste la acción hoy? ")
    if dateIf == "y" or "Y":
        ndate = datetime.today().strftime('%Y-%m-%d')
        file1.writelines("Fecha de Compra: "+ndate+"\n")
    else:
        date = input("Escribe la fecha en que compraste la acción en el siguiente formato Y-M-D (2022-02-28): \n")
        file1.writelines("Fecha de Compra: "+date+"\n")

    file1.writelines("\n")
    file1.writelines("\n")

def call():
    print("call")

def put():
    print("put")

def notaEstructurada():
    print("Nota Estructurada")

def searchAveragePrice():
    file2 = open('portfolio.txt', 'r')
    if 'CME' in file2.read():
        print("true")


if actionType == "1":
    forward()
elif actionType == "2":
    call()
elif actionType == "3":
    notaEstructurada()
elif actionType == "4":
    searchAveragePrice()
else:
    print("Ese producto no existe")


file1.close()