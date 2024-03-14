from PyQt5.QtWidgets import QMessageBox, QApplication
from PyQt5.QtGui import QIcon, QPixmap

iconExito = r'C:\Users\mugui\Documents\Proyectos programacion\PuntoVentaCocina\imagenes\exito.png'
iconError = r'C:\Users\mugui\Documents\Proyectos programacion\PuntoVentaCocina\imagenes\error.png'
iconCerrar = r'C:\Users\mugui\Documents\Proyectos programacion\PuntoVentaCocina\imagenes\cerrado.png'

app = QApplication([])

def msg_info(titulo, mensaje):
    pixmap = QPixmap(iconExito)
    icon = QIcon(pixmap)
    msgBox = QMessageBox()
    msgBox.setWindowIcon(icon)
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setWindowTitle(titulo)
    msgBox.setText(mensaje)
    msgBox.setStandardButtons(QMessageBox.Ok)
    returnValue = msgBox.exec()
    if returnValue == QMessageBox.Ok:
        pass

def msg_error(titulo, mensaje):
    pixmap = QPixmap(iconError)
    icon = QIcon(pixmap)
    msgBox = QMessageBox()
    msgBox.setWindowIcon(icon)
    msgBox.setIcon(QMessageBox.Critical)
    msgBox.setWindowTitle(titulo)
    msgBox.setText(mensaje)
    msgBox.setStandardButtons(QMessageBox.Ok)
    returnValue = msgBox.exec()
    if returnValue == QMessageBox.Ok:
        pass

def msg_cerrar(titulo, mensaje):
    pixmap = QPixmap(iconCerrar)
    pixmapResized = pixmap.scaled(60, 60)
    icon = QIcon(pixmap)
    msgBox = QMessageBox()
    msgBox.setWindowIcon(icon)
    msgBox.setIconPixmap(pixmapResized)  # Establece la imagen en lugar del ícono
    msgBox.setWindowTitle(titulo)
    msgBox.setText(mensaje)
    msgBox.addButton(QMessageBox.Ok)  # Agrega el botón "Aceptar"
    msgBox.addButton(QMessageBox.Cancel)  # Agrega el botón "Cancelar"
    returnValue = msgBox.exec()
    if returnValue == QMessageBox.Ok:
        return True # Llama a la función para realizar la acción deseada

def msg_errorGrave(titulo, error):
    app = QApplication([])

    # Crear un cuadro de diálogo de mensaje
    mensaje = QMessageBox()
    mensaje.setWindowTitle(titulo)
    mensaje.setText(error)
    mensaje.setIcon(QMessageBox.Information)
    mensaje.addButton(QMessageBox.Ok)
    # Mostrar el cuadro de diálogo y esperar a que se cierre
    mensaje.exec_()
    # Cerrar la aplicación
    app.quit()