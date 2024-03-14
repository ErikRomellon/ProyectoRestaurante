from escpos import printer
from datetime import datetime
import mensajebox

try:
    p = printer.Usb(0x04b8, 0x0e15)
    p.set(align='left')
except:
    mensajebox.msg_error("IMPRESORA NO DETECTADA", "ASEGURATE DE TENER ENCENDIDA Y CONECTADA LA IMPRESORA ANTES DE REALIZAR CUALQUIER VENTA. ESTO PODRIA OCASIONAR CIERRES REPENTINOS")

def print_header():
    now = datetime.now()
    formatted_date = now.strftime("%d-%B-%Y  %H:%M:%S")
    rutaImagen = r"C:\Users\mugui\Documents\Proyectos programacion\PuntoVentaCocina\imagenes\logo.jpg"
    p.codepage = 'CP437'
    p._raw('\x1b\x61\x01')
    p.image(rutaImagen)
    p.set(align='center')
    p._raw(b'\x1d\x21\x11')
    p.text("*Cocina Doña Julia*\n")
    p._raw(b'\x1d\x21\x00')
    p.text("C. 53 #369B, Chuminópolis, 97158 Mérida, Yuc.\n")
    p.text(f"{formatted_date}\n")
    p.text("================================================\n")
    p.set(align='left')
    p._raw(b'\x1d\x21\x00')

def print_items(lista):
    p.text("\n")
    for elementos in lista:
        #resultado = ', '.join(elementos)
        p.text(elementos)
        p.text("\n\n")

def print_total(total):
    p.codepage = 'CP437'
    p._raw(b'\x1d\x21\x11')
    p.text(f"\n\n\tTotal: ${total}\n")

def encargo(lista, idcliente, nombre, total):
    print_header()
    p.set(align='left')
    p.text("Tipo de compra: ")
    p._raw(b'\x1d\x21\x10')
    p.text("Encargo\n")
    p._raw(b'\x1d\x21\x00')
    p.text(f"Nº de ticket: {idcliente}\nNombre cliente: {nombre}\n")
    p.text("------------------------------------------------\n")
    p.text("CANTIDAD\tCOMIDA\t\tPRECIO\n")
    print_items(lista)
    print_total(total)

def mostrador(lista, idcliente, total):
    print_header()
    p.set(align='left')
    p.text(f"Tipo de compra: ")
    p._raw(b'\x1d\x21\x10')
    p.text("Mostrador\n")
    p._raw(b'\x1d\x21\x00')
    p.text(f"Nº de ticket: {idcliente}\n")
    p.text("------------------------------------------------\n")
    p.text("CANTIDAD\tCOMIDA\t\tPRECIO\n")
    print_items(lista)
    print_total(total)

def comedor(lista, idcliente, total):
    print_header()
    p.set(align='left')
    p.text("Tipo de compra: ")
    p._raw(b'\x1d\x21\x10')
    p.text("Comedor\n")
    p._raw(b'\x1d\x21\x00')
    p.text(f"Nº de ticket: {idcliente}\n")
    p.text("------------------------------------------------\n")
    p.text("CANTIDAD\tCOMIDA\t\tPRECIO\n")
    print_items(lista)
    print_total(total)

def envio(lista, idcliente, nombre, direccion, referencia, monto, total):
    print_header()
    p.set(align='left')
    p.text("Tipo de compra: ")
    p._raw(b'\x1d\x21\x10')
    p.text("Envío\n")
    p._raw(b'\x1d\x21\x00')
    p.text(f"Nº de ticket: {idcliente}\n")
    p.text("------------------------------------------------\n")
    p.text("CANTIDAD\tCOMIDA\t\tPRECIO\n")
    print_items(lista)
    p.text(f"Nombre: {nombre}\nDireccion:{direccion}\nReferencia: {referencia}\n")
    p.text(f"Envío: ${monto}")
    print_total(total)

def ticketCocina(lista, idcliente,tipo):
    now = datetime.now()
    formatted_date = now.strftime("%d-%B-%Y  %H:%M:%S")
    p.set(align='left')
    p._raw(b'\x1d\x21\x11')
    p.text(f"{formatted_date}\n\n")
    p.set(align='center')
    p._raw(b'\x1d\x21\x11')
    p.text(f"{tipo} - {idcliente}\n")
    p.set(align='left')
    p.text("================================================\n")
    p._raw(b'\x1d\x21\x11')
    nueva_lista = [elemento.rsplit(' - ', 1)[0] for elemento in lista]
    print_items(nueva_lista)

def nota(nota):
    p.codepage = 'CP437'
    p._raw(b'\x1d\x21\x00')
    p.text("------------------------------------------------\n")
    p.text(f"Nota: {nota}\n")

def abrirCajon():
    p.cashdraw(2)

def cortarPapel():
    p.cut()

def imprimir(texto):
    p.set(align='left')
    p._raw(b'\x1d\x21\x00')
    p.text(texto)
    p.text("\n\n")