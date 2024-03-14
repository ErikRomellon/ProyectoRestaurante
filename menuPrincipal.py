"""
PROGRAMA: Programa para gestionar el menú principal el cual contiene todas las funciones para
controlar las ventas y los submenus.
PROGRAMADOR: Erik Jesús Romellón Lorenzana
VERSIÓN 1: escrita el 17 de junio de 2023 por Erik Romellón
REVISIÓN 1.1: 4 de julio de 2023 por Erik Romellón para 
corregir cierres repentinos y agregar la pestaña de "Extras"
PROPÓSITO: Gestionar las ventas de una manera más rapida, genrar tickets de ventas, tener un registro local de todas
las ventas pasadas, gestionar la cartera de clientes e imprimir el corte de ganancias diarias.

"""

from PyQt5.QtCore import QPropertyAnimation, QTimer
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView, QButtonGroup
from PyQt5.uic import loadUi
from datetime import date
import numpy as np

import time
import sys
import CSV
import impresora
import mensajebox

#Clase que controla la ventana principal, se puede abrir el archivo .ui para ver sus componentes internos.
class ventanaPrincipal(QMainWindow):
    def __init__(self):
        super(ventanaPrincipal, self).__init__()
        menuPrincipal = r'C:\Users\mugui\Documents\Proyectos programacion\PuntoVentaCocina\UIs\menu_principal.ui'
        loadUi(menuPrincipal, self)

        self.showMaximized()

        #Variable que controla el numero de ventas diarias.
        global numId
        numId = 1

        #fecha y hora
        self.actualizar_reloj()

        #añadimos nombres a los labels
        menu = CSV.obtenerMenu()
        self.lbl_comida1.setText(menu[0][0])
        self.lbl_comida2.setText(menu[1][0])
        self.lbl_comida3.setText(menu[2][0])
        self.lbl_comida4.setText(menu[3][0])

        #hacemos que las columnas de la tabla ocupen el espacio completo
        self.tabla_ventas.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #tabla_ventas
        self.tabla_historial.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #tabla historial

        #ocultamos cosas
        self.bt_expandir.hide()
        self.cbb_clientesEncargo.hide()
        self.cbb_clientesEnvio.hide()
        self.cbb_costoEnvio.hide()
        self.lbl_corte.hide()#pagina cortes
        self.lbl_eliminarPorID.hide()#pagina historial
        self.lineEdit_IdHistorial.hide()
        self.bt_eliminarHistorial.hide()

        #iniciamos en la pagina de inicio
        self.lbl_dia.setText(date.today().strftime("%d-%b-%Y"))
        self.stackedWidget.setCurrentWidget(self.page_inicio)
        self.llenarCbbClientes()

        #iniciamos la pagina de clientes
        self.llenarCbbExtras()

        #botones frame control
        self.bt_inicio.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_inicio))
        self.bt_extras.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_extras))
        self.bt_clientes.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_clientes))
        self.bt_historial.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_historial))
        self.bt_pagos.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_pagos))
        self.bt_corte.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_corte))

        #control barra de titulos
        self.bt_cerrar.clicked.connect(lambda: self.controlCerrar())
        self.bt_minimizar.clicked.connect(lambda: self.controlMinimizar())
        self.bt_expandir.clicked.connect(lambda: self.controlExpandir())
        self.bt_contraer.clicked.connect(lambda: self.controlContraer())
        self.bt_menu.clicked.connect(lambda: self.moverMenu())

        #botones de compra
        self.bt_media1.clicked.connect(lambda: self.agregarFilaTabla(numId, "Media", menu[0][0], menu[0][1])) #medias
        self.bt_media2.clicked.connect(lambda: self.agregarFilaTabla(numId, "Media", menu[1][0], menu[1][1]))
        self.bt_media3.clicked.connect(lambda: self.agregarFilaTabla(numId, "Media", menu[2][0], menu[2][1]))
        self.bt_media4.clicked.connect(lambda: self.agregarFilaTabla(numId, "Media", menu[3][0], menu[3][1]))
        self.bt_entera1.clicked.connect(lambda: self.agregarFilaTabla(numId, "Entera", menu[0][0], menu[0][2])) #enteras
        self.bt_entera2.clicked.connect(lambda: self.agregarFilaTabla(numId, "Entera", menu[1][0], menu[1][2]))
        self.bt_entera3.clicked.connect(lambda: self.agregarFilaTabla(numId, "Entera", menu[2][0], menu[2][2]))
        self.bt_entera4.clicked.connect(lambda: self.agregarFilaTabla(numId, "Entera", menu[3][0], menu[3][2]))
        #boton agregar extra
        self.bt_agregar.clicked.connect(lambda: self.agregarExtraTabla())

        #botones de cobro
        self.bt_borrar.clicked.connect(lambda: self.eliminarFilaSeleccionada())
        self.bt_cobrar.clicked.connect(lambda: self.btCobrar())

        #botones extras
        self.bt_agregarExtras.clicked.connect(lambda: self.agregarExtra())
        self.bt_eliminarExtras.clicked.connect(lambda: self.eliminarExtra())

        #botones clientes
        self.bt_agregarCliente.clicked.connect(lambda: self.agregarCliente())
        self.bt_eliminarCliente.clicked.connect(lambda: self.eliminarCliente())
        self.btn_verInformacion.clicked.connect(lambda: self.obtenerInfoCliente())

        #botones page_calculadora
        self.bt_cambio.clicked.connect(lambda: self.calcularCambio())
        self.bt_continuar.clicked.connect(lambda: self.realizarCobro())
        self.bt_regresar.clicked.connect(lambda: self.btnRegresar())

        #botones page_historial
        self.bt_buscarDia.clicked.connect(lambda: self.llenarTablaHistorial())
        self.bt_eliminarHistorial.clicked.connect(lambda: self.eliminarVentaPorId())

        #botones page_corte de caja
        self.bt_corteEnvios.clicked.connect(lambda: self.realizarCorteEnvios())
        self.bt_corteCaja.clicked.connect(lambda: self.realizarCorteCaja())
        self.bt_corteTotal.clicked.connect(lambda: self.realizarCorteTotal())

        #eliminar barra y de titulo - opacidad
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)

        #SizeGrip
        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)

        self.frame_superior.mouseMoveEvent = self.moverVentana

        # grupo de checkboxes
        self.button_group = QButtonGroup()
        checkboxes = [self.checkBox_encargo, self.checkBox_mostrador, self.checkBox_comedor, self.checkBox_envio]
        for checkbox in checkboxes:
            self.button_group.addButton(checkbox)
        #boton que
        self.button_group.buttonClicked.connect(self.manejarCheckboxes)
        # manejo de checkboxes
        #esta funcion desactiva los checkboxes que no se encuentran marcados

        if CSV.CrearCSV() == True:
            numId = int(CSV.ultimoId()) + 1

    def manejarCheckboxes(self, button):
        checkboxes = [self.checkBox_encargo, self.checkBox_mostrador, self.checkBox_comedor, self.checkBox_envio]
        for checkbox in checkboxes:
            if checkbox == button:
                checkbox.setChecked(True)
            else:
                checkbox.setChecked(False)
        #verifica que checkbox está marcado para mostrar u ocultar los comboboxes
        if self.checkBox_encargo.isChecked():
            self.cbb_clientesEncargo.show()
            self.cbb_clientesEnvio.hide()
            self.cbb_costoEnvio.hide()
        elif self.checkBox_envio.isChecked():
            self.cbb_clientesEncargo.hide()
            self.cbb_clientesEnvio.show()
            self.cbb_costoEnvio.show()
        else:
            self.cbb_clientesEncargo.hide()
            self.cbb_clientesEnvio.hide()
            self.cbb_costoEnvio.hide()

    #Funcion que muestra relon en lbl_reloj
    def actualizar_reloj(self):
        hora_actual = time.strftime("%H:%M:%S")
        self.lbl_reloj.setText(hora_actual)
        QTimer.singleShot(1000, self.actualizar_reloj)

    def controlCerrar(self):
        if mensajebox.msg_cerrar("Cerrar aplicacion?", "Presiona OK para cerrar") == True:
            self.close()
    
    def controlMinimizar(self):
        self.showMinimized()

    def controlContraer(self):
        self.showNormal()
        self.bt_expandir.show()
        self.bt_contraer.hide()

    def controlExpandir(self):
        self.showMaximized()
        self.bt_contraer.show()
        self.bt_expandir.hide()

    # SizeGrip
    def rezizeEvent(self, event):
        rect = self.rect()
        self.grip.move(rect.right() - self.gripSize, rect.bottom - self.gripSize)

    
    def mousePressEvent(self, event):
        self.click_position = event.globalPos()
    
    # Funcion que permite mover ventana clicando en la parte superior de la ventana
    def moverVentana(self, event):
        if self.isMaximized() == False:
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.click_position)
                self.click_position = event.globalPos()
                event.accept()

            if event.globalPos().y() <= 40:
                self.showMaximized()
                self.bt_expandir.hide()
                self.bt_contraer.show()
            else:
                self.showNormal()
                self.bt_contraer.hide()
                self.bt_expandir.show()

    def moverMenu(self):
        if True:
            width = self.frame_control.width()
            normal = 0
            if width == 0:
                extender = 200
            else:
                extender = normal
            self.animacion = QPropertyAnimation(self.frame_control, b'minimumWidth')
            self.animacion.setDuration(300)
            self.animacion.setStartValue(width)
            self.animacion.setEndValue(extender)
            self.animacion.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animacion.start()

    ###############################################################    Manejo de tablas    ####################################################################################
    def agregarFilaTabla(self, numId, cantidad, comida, precio):
        row = self.tabla_ventas.rowCount()
        self.tabla_ventas.insertRow(row)
        numId = str(numId)
        idItem = QTableWidgetItem(numId)
        cantidadItem = QTableWidgetItem(cantidad)
        comidaItem = QTableWidgetItem(comida)
        precioItem = QTableWidgetItem(precio)
        self.tabla_ventas.setItem(row, 0, idItem)
        self.tabla_ventas.setItem(row, 1, cantidadItem)
        self.tabla_ventas.setItem(row, 2, comidaItem)
        self.tabla_ventas.setItem(row, 3, precioItem)

    def obtenerItemsTabla(self):
        columnas = [1, 2, 3]
        items = []
        for row in range(self.tabla_ventas.rowCount()):
            filaItems = []
            for col in columnas:
                item = self.tabla_ventas.item(row, col)
                if item is not None:
                    filaItems.append(item.text())
            items.append(filaItems)
        return items

    def eliminarFilaSeleccionada(self):
        filaSeleccionada = self.tabla_ventas.currentRow()
        if filaSeleccionada >= 0:
            self.tabla_ventas.removeRow(filaSeleccionada)
            return True
        else:
            mensajebox.msg_error("IMPOSIBLE ELIMINAR", "ASEGURATE DE SELECCIONAR PRIMERO UN ELEMENTO")

    ######################################################       funciones de extras   #############################################################################################
    def llenarCbbExtras(self):
        self.cbb_extras.clear()
        self.cbb_extrasExtras.clear()
        extras = CSV.obtenerExtras()
        extrasSorted = sorted(extras)
        self.cbb_extras.addItems(extrasSorted)
        self.cbb_extrasExtras.addItems(extrasSorted)

    def agregarExtra(self):
        extra = []
        nombre = self.lineEdit_nombreExtras.text()
        precio = self.lineEdit_precioExtras.text()
        if len(nombre) and len(precio) > 0:
            if self.esNumero(precio):
                extra.append(nombre)
                extra.append(precio)
                CSV.agregarExtra(extra)
                self.llenarCbbExtras()
                self.lineEdit_nombreExtras.setText("")
                self.lineEdit_precioExtras.setText("")
                mensajebox.msg_info("Extra agregado!", f"Se ha agregado {nombre} a la lista de extras")
            else:
                mensajebox.msg_error("IMPOSIBLE AGREGAR", "VERIFICA ESCRIBIR UNICAMENTE VALORES NUMERICOS EN EL CAMPO PRECIO")
        else:
            mensajebox.msg_error("IMPOSIBLE AGREGAR", "ASEGURATE DE LLENAR AMBOS CAMPOS")

    def agregarExtraTabla(self):
        extra = self.cbb_extras.currentText()
        informacionExtra = CSV.obtenerInfoExtra(extra)
        self.agregarFilaTabla(numId, "Uno", str(informacionExtra[0]), str(informacionExtra[1]))
        self.cbb_extras.setCurrentIndex(0)

    def eliminarExtra(self):
        extra = self.cbb_extrasExtras.currentText()
        CSV.eliminarExtra(extra)
        self.llenarCbbExtras()
        mensajebox.msg_info("Extra eliminado", "Se ha eliminado " + extra + " de la lista")

    ############################################################    funciones de clientes    #######################################################################################
    def llenarCbbClientes(self):
        self.cbb_clientesClientes.clear()
        self.cbb_clientesEncargo.clear()
        self.cbb_clientesEnvio.clear()
        nombres = CSV.obtenerClientes()
        nombresOrdenados = sorted(nombres)
        # de la pagina incio
        self.cbb_clientesEncargo.addItems(nombresOrdenados)
        self.cbb_clientesEnvio.addItems(nombresOrdenados)
        self.cbb_costoEnvio.setCurrentIndex(0)
        # de la pagina clientes
        self.cbb_clientesClientes.addItems(nombresOrdenados)

    def limpiarPaginaClientes(self):
        self.lbl_nombreClientes.setText("")
        self.lbl_direccionClientes.setText("")
        self.lbl_referenciaClientes.setText("")
        self.lbl_costoEnvioClientes.setText("")
        self.lineEdit_nombre.setText("")
        self.lineEdit_calle.setText("")
        self.lineEdit_numeroCasa.setText("")
        self.lineEdit_cruzamientos.setText("")
        self.lineEdit_colonia.setText("")
        self.lineEdit_referencia.setText("")
        self.lineEdit_costoEnvio.setText("")

    def agregarCliente(self):
        listaCliente=[]
        nombre = self.lineEdit_nombre.text()
        calle = self.lineEdit_calle.text()
        numeroCasa = self.lineEdit_numeroCasa.text()
        cruzamientos = self.lineEdit_cruzamientos.text()
        colonia = self.lineEdit_colonia.text()
        referencia = self.lineEdit_referencia.text()
        costoEnvio = self.lineEdit_costoEnvio.text()

        if calle or numeroCasa or cruzamientos or colonia:
            direccion = "Calle: "+calle + " Numero: " + numeroCasa + " Cruzamientos: " + cruzamientos + " Colonia: " + colonia
        else:
            direccion = ""

        #agregar a la lista
        if len(nombre) > 0:
            listaCliente.append(nombre)
            listaCliente.append(direccion)
            listaCliente.append(referencia)
            listaCliente.append(costoEnvio)
            CSV.agregarCliente(listaCliente)
            self.limpiarPaginaClientes()
            self.llenarCbbClientes()
            mensajebox.msg_info("Cliente agregado con exito!", "Se ha agregado al cliente " + nombre)
        else:
            mensajebox.msg_error("IMPOSIBLE AGREGAR CLIENTE", "ASEGURATE DE ESCRIBIR MINIMO NOMBRE DE CLIENTE")

    def eliminarCliente(self):
        self.limpiarPaginaClientes()
        nombreCliente = self.cbb_clientesClientes.currentText()
        CSV.eliminarCliente(nombreCliente)
        self.llenarCbbClientes()
        mensajebox.msg_info("Cliente eliminado", "Se ha eliminado al cliente " + nombreCliente + " de la lista")

    def obtenerInfoCliente(self):
        self.limpiarPaginaClientes()
        nombreCliente = self.cbb_clientesClientes.currentText()
        if not nombreCliente:
            mensajebox.msg_error("ERROR", "VERIFICA SELECCIONAR PRIMERO UN CLIENTE")
            return
        infoCliente = CSV.obtenerInfoCliente(nombreCliente)
        if len(infoCliente) == 4:
            nombre, direccion, referencia, precioEnvio = map(str, infoCliente[:4])
            if nombre != "nan":
                self.lbl_nombreClientes.setText(nombre)
            if direccion != "nan":
                self.lbl_direccionClientes.setText(direccion)
            if referencia != "nan":
                self.lbl_referenciaClientes.setText(referencia)
            if precioEnvio != "nan":
                self.lbl_costoEnvioClientes.setText(precioEnvio)

    ################################################################     boton cobrar pagina inicio     ############################################################################
    def btCobrar(self):
        compra = self.obtenerItemsTabla()
        #tamaño menor o igual a cero por si las moscas
        if len(compra) <= 0:
            mensajebox.msg_error("IMPOSIBLE REALIZAR COBRO", "ASEGURATE DE AGREGAR ELEMENTOS PARA COBRAR")
            return

        selected_checkbox = self.button_group.checkedButton()

        if selected_checkbox is None:
            mensajebox.msg_error("IMPOSIBLE REALIZAR COBRO", "SELECCIONA TIPO DE COMPRA")
            return

        total = sum(int(elemento[2]) for elemento in compra)
        total = str(total)

        checkbox_text = selected_checkbox.text()

        if checkbox_text == "Encargo":
            self.lbl_info.show()
            self.lbl_informacion.show()
            self.lbl_envioAsignado.hide()
            self.lbl_valorEnvioAsignado.hide()
            nombreClienteEncargo = self.cbb_clientesEncargo.currentText()
            self.lbl_informacion.setText(nombreClienteEncargo)
        elif checkbox_text == "Envío":
            self.lbl_info.show()
            self.lbl_informacion.show()
            self.lbl_envioAsignado.show()
            self.lbl_valorEnvioAsignado.show()
            nombreClienteEnvio = self.cbb_clientesEnvio.currentText()
            datosEnvio = CSV.obtenerInfoCliente(nombreClienteEnvio)
            direccion = datosEnvio[1]
            referencia = datosEnvio[2]
            costoEnvioCliente = datosEnvio[3]
            if isinstance(direccion, str):
                # Verificar si es una cadena vacía
                if not direccion.strip():
                    direccion = "Valor de dirección faltante"
            elif np.isnan(direccion) or not np.isfinite(direccion):
                direccion = "Valor de dirección faltante"

            if isinstance(referencia, str):
                # Verificar si es una cadena vacía
                if not referencia.strip():
                    referencia = "Valor de referencia faltante"
            elif np.isnan(referencia) or not np.isfinite(referencia):
                referencia = "Valor de referencia faltante"

            if isinstance(costoEnvioCliente, str):
                # Verificar si es una cadena vacía
                if not costoEnvioCliente.strip():
                    costoEnvioCliente = "Valor de costo de envío faltante"
            elif np.isnan(costoEnvioCliente) or not np.isfinite(costoEnvioCliente):
                costoEnvioCliente = "Valor de costo de envío faltante"

            # Agregar los valores al label
            self.lbl_informacion.setText(f"Dirección: {direccion}\n Referencia: {referencia}\n Costo de envío: {costoEnvioCliente}")
            costoEnvio = self.cbb_costoEnvio.currentText()
            self.lbl_valorEnvioAsignado.setText("$"+costoEnvio)

            #agregamos el costo de envio seleccionado
            costoEnvio = self.cbb_costoEnvio.currentText()
            total = int(total) + int(costoEnvio)
            total = str(total)

            #mostramos informacion completa del cliente

        else:
            self.lbl_info.hide()
            self.lbl_informacion.hide()
            self.lbl_envioAsignado.hide()
            self.lbl_valorEnvioAsignado.hide()
        self.frame_control.setProperty(b"minimumWidth", 0)
        self.bt_menu.setDisabled(True)

        #se muestra la pagina calculadora
        self.stackedWidget.setCurrentWidget(self.page_calculadora)
        self.lbl_precio.setText(total)
        self.lbl_cambioTexto.hide()
        self.lbl_cambio.hide()

    ###################################################################   funciones pagina calculadora    #####################################################################

    #boton regresar pagina calculadora
    def btnRegresar(self):
        self.bt_menu.setEnabled(True)
        self.stackedWidget.setCurrentWidget(self.page_inicio)

    #funcion para calular cambio en la pagina calculadora
    def calcularCambio(self):
        precio = self.lbl_precio.text()
        pago = self.lineEdit_pago.text()
        if pago:
            if int(pago) > int(precio):
                cambio = int(pago) - int(precio)
                self.lbl_cambioTexto.show()
                self.lbl_cambio.show()
                self.lbl_cambio.setText(str(cambio))
            else:
                self.lineEdit_pago.setText("")
                mensajebox.msg_error("IMPOSIBLE CALCULAR CAMBIO", "LA CANTIDAD A COBRAR DEBE SER MAYOR AL TOTAL")
        else:
            mensajebox.msg_error("IMPOSIBLE CALCULAR CAMBIO", "AGREGA PRIMERO LA CANTIDAD DE PAGO")

    #boton siguiente en la pagina de calculadora
    def realizarCobro(self):
        global numId
        compra = self.obtenerItemsTabla()
        compraSinModificar = self.obtenerItemsTabla()
        nota = self.textEdit_nota.toPlainText()
        total = self.lbl_precio.text()
        nueva_lista = [f"{elemento[0]} - {elemento[1]} - ${elemento[2]}" for elemento in compra]
        selected_checkbox = self.button_group.checkedButton()

        if selected_checkbox is None:
            self.stackedWidget.setCurrentWidget(self.page_inicio)
            mensajebox.msg_error("ADVERTENCIA", "POR ALGUN MOTIVO NO SE SELEECIONÓ NIGUN TIPO DE COMPRA, REALIZA DE NUEVO LA OPERACION DE VENTA")
            return

        metodoDePago = "Tarjeta" if self.checkBox_pagoTarjeta.isChecked() else "Efectivo"

        self.cbb_clientesEncargo.hide()
        self.cbb_clientesEnvio.hide()
        self.cbb_costoEnvio.hide()

        if selected_checkbox == self.checkBox_encargo:
            nombre = self.cbb_clientesEncargo.currentText()
            tipo = "ENCARGO"
            #impresora.encargo(nueva_lista, str(numId), nombre, str(total))

        elif selected_checkbox == self.checkBox_mostrador:
            tipo = "MOSTRADOR"
            nombre = "Cliente"+str(numId)
            #impresora.mostrador(nueva_lista, numId, total)
            #impresora.cortarPapel()
            #impresora.ticketCocina(nueva_lista, numId, tipo)

        elif selected_checkbox == self.checkBox_comedor:
            tipo = "COMEDOR"
            nombre = "Cliente " + str(numId)
            #impresora.comedor(nueva_lista, numId, total)
            #impresora.cortarPapel()
            #impresora.ticketCocina(nueva_lista, numId, tipo)

        elif selected_checkbox == self.checkBox_envio:
            nombre = self.cbb_clientesEnvio.currentText()
            datosEnvio = CSV.obtenerInfoCliente(nombre)
            direccion = datosEnvio[1]
            referencia = datosEnvio[2]
            costoEnvio = self.cbb_costoEnvio.currentText()
            tipo = "ENVIO"
            #impresora.envio(nueva_lista, numId, nombre, direccion, referencia, costoEnvio, total)


        if len(nota) > 0:
            #impresora.nota(nota)
            self.textEdit_nota.clear()
        #impresora.cortarPapel()

        #agrega los elementos comprados a la tabla del día
        for elements in compraSinModificar:
            listaHistorial = []
            listaHistorial.append(numId)
            listaHistorial.append(nombre)
            listaHistorial.extend(elements)
            listaHistorial.append(tipo)
            listaHistorial.append(metodoDePago)
            CSV.agregarElementosHistorial(listaHistorial)

        self.lineEdit_pago.setText("")
        self.tabla_ventas.setRowCount(0)
        self.llenarCbbClientes()
        self.bt_menu.setEnabled(True)
        self.button_group.setExclusive(False)

        for checkbox in self.button_group.buttons():
            checkbox.setChecked(False)

        self.checkBox_pagoTarjeta.setChecked(False)
        self.stackedWidget.setCurrentWidget(self.page_inicio)
        numId += 1

    ###################################################################   funciones pagina historial    #####################################################################
    def llenarTablaHistorial(self):
        self.tabla_historial.clearContents()
        self.tabla_historial.setRowCount(0)
        fecha = self.obtenerFechaSeleccionada()
        encabezado, datos, existe = CSV.obtenerVentaDiaria(fecha)
        if fecha == date.today().strftime("%d-%m-%Y"):
            self.lbl_eliminarPorID.show()
            self.lineEdit_IdHistorial.show()
            self.bt_eliminarHistorial.show()
        else:
            self.lbl_eliminarPorID.hide()
            self.lineEdit_IdHistorial.hide()
            self.bt_eliminarHistorial.hide()
        if existe == True:
            self.tabla_historial.setRowCount(len(datos))
            self.tabla_historial.setColumnCount(len(encabezado))
            # Establecer el encabezado de la tabla
            self.tabla_historial.setHorizontalHeaderLabels(encabezado)
            # Agregar los datos a la tabla
            for fila, datos_fila in enumerate(datos):
                for columna, dato in enumerate(datos_fila):
                    item = QTableWidgetItem(dato)
                    self.tabla_historial.setItem(fila, columna, item)
        else:
            mensajebox.msg_error("ARCHIVO INEXISTENTE", f"SELECCIONA UN DIA CON REGISTRO PREVIO DE VENTAS, EL DIA {fecha} NO TIENE REGISTRO DE VENTAS")

    def obtenerFechaSeleccionada(self):
        fecha = self.calendarWidget.selectedDate()
        fecha_str = fecha.toString("dd-MM-yyyy")
        return fecha_str

    def eliminarVentaPorId(self):
        idEliminar = self.lineEdit_IdHistorial.text()
        dia = date.today().strftime("%d-%m-%Y")
        filasEliminadas = CSV.eliminarFilasPorId(dia, idEliminar)
        if filasEliminadas > 0:
            self.llenarTablaHistorial()
            self.lineEdit_IdHistorial.setText("")
            mensajebox.msg_info(f"Id {idEliminar} ha sido eliminado", f"Se han eliminado {filasEliminadas} filas")
        else:
            mensajebox.msg_error("NO SE HA ELIMINADO NINGUN ELEMENTO", "ASEGURATE DE ESCRIBIR UN ID EN EL RANGO DE LA LISTA")

    ###################################################################   funciones pagina cortes  #####################################################################
    def realizarCorteEnvios(self):
        self.lbl_corte.show()
        dia = date.today().strftime("%d-%m-%Y")
        suma_total, totales_envio, total_tarjeta = CSV.obtenerTotalesEnvio(dia)
        #impresora.imprimir('Corte de caja dia: '+ dia)
        for persona in totales_envio.values():
            nombre = persona['nombre']
            total = persona['total']
            metodo_pago = persona['metodo_pago']
            texto = f"{nombre} - $ {total} - Metodo de pago: {metodo_pago}"
            #impresora.imprimir(texto)
        #impresora.imprimir("\n\tTotal: $" + str(suma_total))
        #impresora.cortarPapel()
        self.lbl_corte.setText(f"ENVIOS\n\nEl total de los envios en efectivo fue: ${suma_total}, El total de los pagos con tarjeta fue ${total_tarjeta}")

    def realizarCorteCaja(self):
        self.lbl_corte.show()
        dia = date.today().strftime("%d-%m-%Y")
        efectivo, tarjeta = CSV.obtenerSumaPreciosSinEnvio(dia)
        self.lbl_corte.setText(f"CAJA\n\nGanancias en efectivo contemplando ventas Encargo, Mostrador, Comedor es: ${efectivo}\n\nVentas efectuadas en tarjeta: ${tarjeta}")

    def realizarCorteTotal(self):
        self.lbl_corte.show()
        total = CSV.calcularTotalPrecios(date.today().strftime("%d-%m-%Y"))
        self.lbl_corte.setText(f"TOTAL\n\nGanancia total contemplando ventas tipo Encargo, Mostrador, Comedor y Envio es: ${total}\n\nNOTA: LAS GANANCIAS CON EL METODO DE PAGO TARJETA ESTÁN CONTEMPLADOS EN EL TOTAL")

    ###################################################################   funciones adicionales    #####################################################################
    def esNumero(self, valor):
        try:
            float(valor)
            return True
        except ValueError:
            return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mi_app = ventanaPrincipal()
    mi_app.show()
    sys.exit(app.exec_())