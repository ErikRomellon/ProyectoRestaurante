from datetime import datetime
import csv
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication

import CSV
import mensajebox
from menuPrincipal import ventanaPrincipal

app: QApplication = QtWidgets.QApplication([])

#Elementos ui
crearMenu = uic.loadUi(r'C:\Users\mugui\Documents\Proyectos programacion\PuntoVentaCocina\UIs\creacion_menu.ui')
rutaComida = r"C:\Users\mugui\Documents\Proyectos programacion\PuntoVentaCocina\csv\Comidas.csv"

#Lista de comidas existentes para llenar los cbb
listaComidas = []
listaCSV=[]

#Se almacena el valor del día en formato dd-mm-yyyy
now = datetime.now()
tiempo = now.strftime("%d-%m-%Y")

#Llena datos de los cbb
def LlenaDatosCbb():
    listaComidas.clear()
    try:
        with open(rutaComida, "r") as csvfile:
            lector = csv.reader(csvfile)
            lector = sorted(lector, reverse=False)
            for row in lector:
                listaComidas.append(row[0])
            crearMenu.cbbComida_1.addItems(listaComidas)
            crearMenu.cbbComida_2.addItems(listaComidas)
            crearMenu.cbbComida_3.addItems(listaComidas)
            crearMenu.cbbComida_4.addItems(listaComidas)
        crearMenu.lblTextoFecha.setText("Ingresa menú del día " + tiempo)
    except FileNotFoundError:
        mensajebox.msg_error("ERROR GRAVE!", f"IMPOSIBLE ENCONTRAR LA RUTA: {rutaComida} \n\nCONTACTA A SOPORTE PARA ARREGLAR EL FALLO \n(CON UN COSTO DE $1000) :D")
        app.closeAllWindows()

#AgregaComida al csv comidas (donde está toda la lista)
def CrearComida():
    if rutaComida:
        comidaNueva = crearMenu.txtNuevaComida.text()
        with open(rutaComida, 'r') as file:
            reader = csv.reader(file)
            listaComidasCsv = []
            for row in reader:
                listaComidasCsv.append(row[0])
            if listaComidasCsv.count(comidaNueva.lower().capitalize()) > 0:
                mensajebox.msg_error("ERROR!", "EL ELEMENTO QUE QUIERES AGREGAR YA EXISTE EN LA LISTA DE COMIDAS!")
            else:
                if len(comidaNueva) > 0:
                    file = open(rutaComida, "a")
                    file.write("\n"+comidaNueva.lower().capitalize())
                    file.close()
                    crearMenu.txtNuevaComida.setText("")
                    crearMenu.cbbComida_1.clear()
                    crearMenu.cbbComida_2.clear()
                    crearMenu.cbbComida_3.clear()
                    crearMenu.cbbComida_4.clear()
                    LlenaDatosCbb()
                    mensajebox.msg_info("Agregado!", f"Se ha agregado a la lista: \n{comidaNueva.lower().capitalize()}")
                else:
                    mensajebox.msg_error("ERROR!", "IMPOSIBLE AÑADIR UN ELEMENTO VACIO!")
    else:
        mensajebox.msg_error("ERROR GRAVE!", f"IMPOSIBLE ENCONTRAR LA RUTA: {rutaComida} CONTACTA A SOPORTE :D")
        
def agregarComida(comidaSeleccionada, precioMedia, precioEntera, gbComida, labelAgregada):
    listaCSV.clear()

    if len(comidaSeleccionada) == 0 or len(precioMedia) == 0 or len(precioEntera) == 0:
        mensajebox.msg_error("ERROR!", "Rellena ambos campos para poder agregar los precios")
    else:
        gbComida.setVisible(False)
        labelAgregada.setVisible(True)
        labelAgregada.setText(f"{comidaSeleccionada.upper()}\nHA SIDO AGREGADO")
        mensajebox.msg_info("Exito!",f"{comidaSeleccionada} agregada con exito!")
        listaCSV.append(comidaSeleccionada)
        listaCSV.append(precioMedia)
        listaCSV.append(precioEntera)
        CSV.AgregarElementoMenu(listaCSV)

def AgregarComida1():
    agregarComida(crearMenu.cbbComida_1.currentText(), crearMenu.txtPrecioMedia_1.text(), crearMenu.txtPrecioEntera_1.text(), crearMenu.gbComida_1, crearMenu.label_agregada_1)
    totalFilas = CSV.ContarFilas()
    if(totalFilas == 4):
        crearMenu.btnSiguiente.show()

def AgregarComida2():
    agregarComida(crearMenu.cbbComida_2.currentText(), crearMenu.txtPrecioMedia_2.text(), crearMenu.txtPrecioEntera_2.text(), crearMenu.gbComida_2, crearMenu.label_agregada_2)
    totalFilas = CSV.ContarFilas()
    if(totalFilas == 4):
        crearMenu.btnSiguiente.show()

def AgregarComida3():
    agregarComida(crearMenu.cbbComida_3.currentText(), crearMenu.txtPrecioMedia_3.text(), crearMenu.txtPrecioEntera_3.text(), crearMenu.gbComida_3, crearMenu.label_agregada_3)
    totalFilas = CSV.ContarFilas()
    if(totalFilas == 4):
        crearMenu.btnSiguiente.show()

def AgregarComida4():
    agregarComida(crearMenu.cbbComida_4.currentText(), crearMenu.txtPrecioMedia_4.text(), crearMenu.txtPrecioEntera_4.text(), crearMenu.gbComida_4, crearMenu.label_agregada_4)
    totalFilas = CSV.ContarFilas()
    if(totalFilas == 4):
        crearMenu.btnSiguiente.show()

def siguiente():
    comillas = '"'
    #Excepcion aqui
    totalFilas = CSV.ContarFilas()
    if(totalFilas == 4):
        crearMenu.close()
        ventanaPrincipal().show()
    else:
        mensajebox.msg_error("IMPOSIBLE CONTINUAR!", f"PRESIONA {comillas}REESTABLECER MENÚ{comillas} PARA CREAR UN MENÚ NUEVO, EL MENÚ ACTUAL TIENE {totalFilas} ITEMS AGREGADOS")


def reiniciar():
    CSV.reiniciarMenu()
    crearMenu.btnSiguiente.hide()
    
    for i in range(1, 5):
        getattr(crearMenu, f"gbComida_{i}").setVisible(True)
        getattr(crearMenu, f"label_agregada_{i}").setVisible(False)
        getattr(crearMenu, f"txtPrecioMedia_{i}").setText("")
        getattr(crearMenu, f"txtPrecioEntera_{i}").setText("")
        getattr(crearMenu, f"cbbComida_{i}").clear()
    LlenaDatosCbb()
    mensajebox.msg_info("Aviso!", "Se ha reestablecido el menu previamente creado, favor de rellenar los campos con los nuevos datos")

crearMenu.show()#abrimos el ui menú
LlenaDatosCbb()#llenamos los cbb con las comidas existentes
crearMenu.btnSiguiente.hide()

if CSV.CrearCSV() == True:
    crearMenu.btnReiniciar.setText("Reestablecer\nmenú")

totalFilas = CSV.ContarFilas()
if(totalFilas == 4):
    crearMenu.btnSiguiente.show()

#Botones
button_functions = {
    crearMenu.btnCrearComida: CrearComida,
    crearMenu.btnAgregarComida_1: AgregarComida1,
    crearMenu.btnAgregarComida_2: AgregarComida2,
    crearMenu.btnAgregarComida_3: AgregarComida3,
    crearMenu.btnAgregarComida_4: AgregarComida4,
    crearMenu.btnSiguiente: siguiente,
    crearMenu.btnReiniciar: reiniciar
}

for button, function in button_functions.items():
    button.clicked.connect(function)

#Ejecucion de la app
app.exec()