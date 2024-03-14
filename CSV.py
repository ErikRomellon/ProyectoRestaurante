import csv, shutil
from datetime import datetime
import sys, os
import mensajebox
from csv import writer
import pandas as pd
from csv import reader, DictReader

#Se almacena el valor del día en formato dd-mm-yyyy
now = datetime.now()
tiempo = now.strftime("%d-%m-%Y")

#Ruta de documentos csv
rutaRegistro = r"C:\Users\mugui\Documents\Proyectos programacion\PuntoVentaCocina\csv\historialVentas\ "
rutaMenu = r"C:\Users\mugui\Documents\Proyectos programacion\PuntoVentaCocina\csv\menusDiarios\ "
rutaClientes = r"C:\Users\mugui\Documents\Proyectos programacion\PuntoVentaCocina\csv\Clientes.csv"
rutaExtras = r"C:\Users\mugui\Documents\Proyectos programacion\PuntoVentaCocina\csv\Extras.csv"

def CrearCSV():
    ruta_archivo = rutaMenu[:-1] + "menu" + tiempo + ".csv"
    if os.path.exists(ruta_archivo):
        return True
    else:
        try:
            file = open(rutaRegistro[:-1] + tiempo + ".csv", "w", newline='', encoding='utf-8') #segun a para escibir en un doc creado
            file.write("Id_cliente,Nombre_cliente,Cantidad,Comida,Precio,Tipo_compra,Metodo_pago\n")
            file.close()
        except FileNotFoundError:
            mensajebox.msg_error("EL DIRECTORIO NO EXISTE!", "IMPOSIBLE CREAR DOCUMENTO DE REGISTRO, CREA LA CARPETA CORRESPONDIENTE")
            sys.exit()

        try:
            file = open(rutaMenu[:-1] + "menu" + tiempo + ".csv", "w", newline='', encoding='utf-8')
            file.write("COMIDAS,PRECIO_MEDIA,PRECIO_ORDEN" + "\n")
            file.close()
        except FileNotFoundError:
            mensajebox.msg_error("EL DIRECTORIO NO EXISTE!", "IMPOSIBLE CREAR DOCUMENTO DE MENU DIARIO, CREA LA CARPETA CORRESPONDIENTE")
            sys.exit()

def reiniciarMenu():
    try:
        file = open(rutaMenu[:-1] + "menu" + tiempo + ".csv", "w", newline='', encoding='utf-8')
        file.write("COMIDAS,PRECIO_MEDIA,PRECIO_ORDEN" + "\n")
        file.close()
    except FileNotFoundError:
        mensajebox.msg_error("EL DIRECTORIO NO EXISTE!", "IMPOSIBLE CREAR DOCUMENTO DE MENU DIARIO, CREA LA CARPETA CORRESPONDIENTE")
        sys.exit()

def ultimoId():
    ruta_archivo = rutaRegistro[:-1] + tiempo + ".csv"
    with open(ruta_archivo, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            id_cliente = row[0]
        ultimo_id_cliente = id_cliente
        if ultimo_id_cliente == "Id_cliente":
            ultimo_id_cliente = 0
    return ultimo_id_cliente

################   funciones para csv menu   #####################

def AgregarElementoMenu(lista):
    if os.path.exists(rutaMenu[:-1] + "menu" +(tiempo) + ".csv"):
        with open(rutaMenu[:-1] + "menu" +(tiempo) + ".csv", "a", newline='', encoding='utf-8') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(lista)
            f_object.close()

def obtenerMenu(): #Lee el archivo menuXXXXXX y retorna elementos nombre, precios
    menu = []
    try:
        with open(rutaMenu[:-1] + "menu" + tiempo + ".csv", 'r', newline='', encoding='utf-8') as read_obj:
            csv_reader = reader(read_obj)
            header = next(csv_reader)
            if header != None:
                for row in csv_reader:
                    menu.append(row)
            return menu
    except FileNotFoundError:
        mensajebox.msg_error("EL ARCHIVO DEL MENU NO FUE ENCONTRADO", "IMPOSIBLE OBTENER MENU DIARIO, CREALO NUEVAMENTE")

def ContarFilas():
    df = pd.read_csv(rutaMenu[:-1] + "menu" +tiempo + ".csv")
    total_rows = len(df.axes[0])
    return total_rows

################   funciones para csv clientes   #####################
def agregarCliente(datos):
    try:
        data_frame = pd.read_csv(rutaClientes)
        # Crear un nuevo DataFrame con los nuevos datos
        nuevos_datos = {
            "NOMBRE": [datos[0]],
            "DIRECCION": [datos[1]],
            "REFERENCIA": [datos[2]],
            "COSTO_ENVIO": [datos[3]]
        }
        data_frame_nuevos = pd.DataFrame(nuevos_datos)
        # Concatenar el DataFrame existente con los nuevos datos
        data_frame_actualizado = pd.concat([data_frame, data_frame_nuevos])
        data_frame_actualizado.to_csv(rutaClientes, index=False)
    except FileNotFoundError:
        mensajebox.msg_error("EL ARCHIVO Clientes.csv NO FUE ENCONTRADO", "IMPOSIBLE AGREGAR UN CLIENTE NUEVO")

def eliminarCliente(nombreBuscado):
    try:
        data_frame = pd.read_csv(rutaClientes, skipinitialspace=True)
        # Elimina la fila con el nombre buscado
        data_frame = data_frame[data_frame["NOMBRE"].str.strip() != nombreBuscado]
        # Guarda el DataFrame actualizado en el archivo CSV
        data_frame.to_csv(rutaClientes, index=False)
    except FileNotFoundError:
        mensajebox.msg_error("EL ARCHIVO Clientes.csv NO FUE ENCONTRADO", "IMPOSIBLE ELIMINAR AL CLIENTE")

def obtenerClientes():
    data_frame = pd.read_csv(rutaClientes)  # Lee el archivo CSV y crea un DataFrame
    nombres = data_frame["NOMBRE"].tolist()
    return nombres

def obtenerInfoCliente(nombreBuscar):
    data_frame = pd.read_csv(rutaClientes)
    fila_encontrada = data_frame.loc[data_frame["NOMBRE"] == nombreBuscar]
    valores_fila = fila_encontrada.values.tolist()[0]
    return valores_fila

################   funciones para csv extras   #####################

def agregarExtra(datos):
    try:
        data_frame = pd.read_csv(rutaExtras)
        # Crear un nuevo DataFrame con los nuevos datos
        nuevos_datos = {
            "NOMBRE": [datos[0]],
            "PRECIO": [datos[1]],
        }
        data_frame_extras = pd.DataFrame(nuevos_datos)
        # Concatenar el DataFrame existente con los nuevos datos
        data_frame_actualizado = pd.concat([data_frame, data_frame_extras])
        data_frame_actualizado.to_csv(rutaExtras, index=False)
    except FileNotFoundError:
        mensajebox.msg_error("EL ARCHIVO Extras.csv NO FUE ENCONTRADO", "IMPOSIBLE AGREGAR UN EXTRA NUEVO")

def obtenerExtras():
    data_frame = pd.read_csv(rutaExtras)  # Lee el archivo CSV y crea un DataFrame
    extras = data_frame["NOMBRE"].tolist()
    return extras

def eliminarExtra(nombre):
    df = pd.read_csv(rutaExtras)
    df.drop(df[df['NOMBRE'] == nombre].index, inplace=True)
    df.to_csv(rutaExtras, index=False)

def obtenerInfoExtra(nombreBuscar):
    data_frame = pd.read_csv(rutaExtras)
    fila_encontrada = data_frame.loc[data_frame["NOMBRE"] == nombreBuscar]
    valores_fila = fila_encontrada.values.tolist()[0]
    return valores_fila


################   funciones para historial ventas   #####################

def agregarElementosHistorial(lista):
    ruta_archivo = rutaRegistro[:-1] + tiempo + ".csv"
    if os.path.exists(ruta_archivo):
        with open(rutaRegistro[:-1] + tiempo + ".csv", "a", newline='', encoding='utf-8') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(lista)
            f_object.close()

def obtenerVentaDiaria(fecha):
    datos = []
    if os.path.exists(rutaRegistro[:-1] + fecha + ".csv"):
        with open(rutaRegistro[:-1] + fecha + ".csv") as archivo:
            reader = csv.reader(archivo)
            encabezado = next(reader)

            for fila in reader:
                datos.append(fila)
        return encabezado, datos, True
    else:
        return "", "", False

def eliminarFilasPorId(fecha, id_a_eliminar):
    archivo = rutaRegistro[:-1] + fecha + ".csv"
    archivo_temporal = rutaRegistro[:-1] + "temp.csv"
    filasEliminadas = 0
    with open(archivo, "r") as archivo_entrada, open(archivo_temporal, "w", newline="") as archivo_temp:
        lector_csv = csv.reader(archivo_entrada)
        escritor_csv = csv.writer(archivo_temp)
        # Recorrer las filas del archivo de entrada y escribir solo las filas que no tienen el id a eliminar
        for fila in lector_csv:
            if fila[0] != str(id_a_eliminar):
                escritor_csv.writerow(fila)
            else:
                filasEliminadas += 1
    shutil.move(archivo_temporal, archivo)
    return filasEliminadas

################   funciones para cortes de caja   #####################
def obtenerTotalesEnvio(fecha):
    totales_envio = {}
    suma_total = 0
    totales_envio_tarjeta = {}
    suma_total_tarjeta = 0

    with open(rutaRegistro[:-1] + fecha +".csv", newline='') as archivo:
        reader = csv.DictReader(archivo)
        for fila in reader:
            id_cliente = fila['Id_cliente']
            nombre_cliente = fila['Nombre_cliente']
            tipo_compra = fila['Tipo_compra']
            metodo_pago = fila['Metodo_pago']
            precio = float(fila['Precio'])
            if tipo_compra == 'ENVIO':
                if id_cliente not in totales_envio:
                    if metodo_pago == 'Tarjeta':
                        totales_envio[id_cliente] = {'nombre': nombre_cliente, 'total': 0,'metodo_pago': 'Tarjeta'}
                        totales_envio_tarjeta[id_cliente] = {'nombre': nombre_cliente, 'total': precio, 'metodo_pago': 'Tarjeta'}
                    else:
                        totales_envio[id_cliente] = {'nombre': nombre_cliente, 'total': precio, 'metodo_pago': 'Efectivo'}
                else:
                    if metodo_pago != 'Tarjeta':
                        totales_envio[id_cliente]['total'] += precio
                    else:
                        totales_envio_tarjeta[id_cliente]['total'] += precio


    for persona in totales_envio.values():
        suma_total += persona['total']
    for persona in totales_envio_tarjeta.values():
        suma_total_tarjeta += persona['total']

    return suma_total, totales_envio, suma_total_tarjeta

def obtenerSumaPreciosSinEnvio(tiempo):
    suma_efectivo = 0
    suma_tarjeta = 0

    with open(rutaRegistro[:-1] + tiempo + ".csv", newline='') as archivo:
        reader = csv.DictReader(archivo)
        for fila in reader:
            tipo_compra = fila['Tipo_compra']
            metodo_pago = fila['Metodo_pago']
            precio = float(fila['Precio'])

            if tipo_compra != 'ENVIO':
                if metodo_pago == 'Efectivo':
                    suma_efectivo += precio
                elif metodo_pago == 'Tarjeta':
                    suma_tarjeta += precio

    return suma_efectivo, suma_tarjeta

def calcularTotalPrecios(dia):
    total = 0
    with open(rutaRegistro[:-1] + dia + ".csv", newline='') as archivo:
        reader = csv.DictReader(archivo)
        for fila in reader:
            precio = float(fila['Precio'])
            total += precio
        #cerrar archivo aqui
    return total

