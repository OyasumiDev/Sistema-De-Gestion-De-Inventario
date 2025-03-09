import sqlite3
from datetime import datetime, timedelta
from typing import Optional, Union
import pandas as pd
from tabulate import tabulate
import math
import random

def crear_conexion() -> sqlite3.Connection:
    try:
        conn = sqlite3.connect('inventario.db')
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        raise

def crear_tablas():
    conn = crear_conexion()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Productos (
        id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_producto TEXT,
        precio REAL,
        stock_actual INTEGER DEFAULT 0,
        stock_seguridad INTEGER,
        punto_reorden INTEGER,
        proveedor_id INTEGER,
        clasificacion_abc TEXT,
        eoq INTEGER,
        costo_pedido REAL,
        costo_almacenamiento REAL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Proveedores (
        id_proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_proveedor TEXT,
        contacto TEXT,
        telefono TEXT,
        email TEXT,
        pais TEXT,
        tiempo_entrega INTEGER
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Pedidos (
        id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
        id_producto INTEGER,
        cantidad_pedida INTEGER,
        fecha_pedido DATE,
        fecha_entrega DATE,
        estado_pedido TEXT,
        FOREIGN KEY(id_producto) REFERENCES Productos(id_producto)
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Historial_Inventario (
        id_historial INTEGER PRIMARY KEY AUTOINCREMENT,
        id_producto INTEGER,
        cantidad INTEGER,
        tipo_movimiento TEXT,
        fecha_movimiento DATE,
        razon TEXT,
        FOREIGN KEY(id_producto) REFERENCES Productos(id_producto)
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Demanda_Promedio (
        id_demanda INTEGER PRIMARY KEY AUTOINCREMENT,
        id_producto INTEGER,
        demanda_diaria INTEGER,
        demanda_mensual INTEGER,
        fecha_registro DATE,
        FOREIGN KEY(id_producto) REFERENCES Productos(id_producto)
    )''')

    conn.commit()
    conn.close()

def insertar_datos_prueba():
    conn = crear_conexion()
    cursor = conn.cursor()

    proveedores = []
    for i in range(1, 51):
        proveedores.append(( 
            f'Proveedor {i}',
            f'Contacto {i}',
            f'555-1{i}23{i}',
            f'contacto{i}@proveedor{i}.com',
            random.choice(['México', 'Estados Unidos', 'Canadá', 'Argentina', 'Colombia']),
            random.randint(1, 10)
        ))

    cursor.executemany('''INSERT INTO Proveedores (nombre_proveedor, contacto, telefono, email, pais, tiempo_entrega)  
                        VALUES (?, ?, ?, ?, ?, ?)''', proveedores)

    productos = []
    productos_cristal = [
        "Vaso de cristal transparente", "Plato de cristal blanco", "Jarrón de cristal azul",
        "Copa de vino de cristal rojo", "Taza de cristal verde", "Botella de cristal ámbar",
        "Vasija de cristal morado", "Vaso de cristal negro", "Cristal decorativo rosa",
        "Lámpara de cristal esmeralda", "Frasco de cristal de color ámbar", "Cristal grabado transparente",
        "Copas de cristal opalescente", "Plato hondo de cristal verde lima", "Vaso de cristal turquesa",
        "Cristales de ventana de cristal blanco puro", "Adorno de cristal color rubí", "Candelabro de cristal púrpura",
        "Vasitos de cristal celeste", "Espejo de cristal azulado", "Lentes de gafas de cristal plateado",
        "Botella de cristal transparente con tapa dorada", "Jarrón de cristal verde oliva", "Frascos decorativos de cristal naranja",
        "Taza de cristal transparente con borde dorado", "Vaso de cristal opaco negro", "Cristales de vidrio teñido en rojo",
        "Vasija de cristal rosado", "Plato de cristal negro", "Copas de champán de cristal verde", 
        "Vaso de cristal con detalles en plata", "Botellas de cristal marrón para aceite", "Candelabro de cristal blanco mate",
        "Adorno de cristal esmeralda con detalles en oro", "Vaso de cristal con acabado iridiscente", 
        "Taza de cristal turquesa con detalles plateados", "Cristales decorativos en tonos lilas", "Jarrón de cristal azul celeste",
        "Plato de cristal con acabado metálico plateado", "Vasija de cristal transparente con borde pintado", 
        "Copa de cristal rosa pálido", "Plato de cristal con efecto espejo", "Vaso de cristal gris ahumado",
        "Frasco de cristal para conservas con tapa roja", "Vasitos de cristal multicolor", "Copa de cristal con detalles en cristal rojo",
        "Adorno de cristal verde esmeralda", "Lámpara de cristal transparente con detalles azules", 
        "Plato de cristal transparente con pintura dorada", "Vasija de cristal púrpura con detalles plateados"
    ]

    for i, nombre_producto in enumerate(productos_cristal, start=1):
        costo_pedido = round(random.uniform(5.0, 20.0), 2)
        costo_almacenamiento = round(random.uniform(1.0, 5.0), 2)
        productos.append((
            nombre_producto,
            round(random.uniform(40.0, 100.0), 2),
            random.randint(5, 20),
            random.randint(2, 10),
            random.randint(10, 20),
            random.randint(1, 50),
            random.choice(['A', 'B', 'C']),
            random.randint(10, 30),
            costo_pedido,
            costo_almacenamiento
        ))

    cursor.executemany('''INSERT INTO Productos (nombre_producto, precio, stock_actual, stock_seguridad, punto_reorden, proveedor_id, clasificacion_abc, eoq, costo_pedido, costo_almacenamiento)  
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', productos)

    pedidos = []
    for _ in range(50):
        id_producto = random.randint(1, 50)
        cantidad_pedida = random.randint(1, 10)
        fecha_pedido = datetime.now().date()
        fecha_entrega = fecha_pedido + timedelta(days=random.randint(1, 7))
        estado_pedido = random.choice(['Pendiente', 'Enviado', 'Entregado'])

        pedidos.append((id_producto, cantidad_pedida, fecha_pedido, fecha_entrega, estado_pedido))

    cursor.executemany('''INSERT INTO Pedidos (id_producto, cantidad_pedida, fecha_pedido, fecha_entrega, estado_pedido)  
                        VALUES (?, ?, ?, ?, ?)''', pedidos)

    historial_inventario = []
    for _ in range(50):
        id_producto = random.randint(1, 50)
        cantidad = random.randint(1, 10)
        tipo_movimiento = random.choice(['Entrada', 'Salida'])
        fecha_movimiento = datetime.now().date()
        razon = random.choice(['Compra', 'Venta', 'Devolución', 'Ajuste'])

        historial_inventario.append((id_producto, cantidad, tipo_movimiento, fecha_movimiento, razon))

    cursor.executemany('''INSERT INTO Historial_Inventario (id_producto, cantidad, tipo_movimiento, fecha_movimiento, razon)  
                        VALUES (?, ?, ?, ?, ?)''', historial_inventario)

    demandas = []
    for i in range(1, 51):
        demandas.append((
            i,
            random.randint(1, 10),
            random.randint(30, 300),
            datetime.now().date()
        ))

    cursor.executemany('''INSERT INTO Demanda_Promedio (id_producto, demanda_diaria, demanda_mensual, fecha_registro)  
                        VALUES (?, ?, ?, ?)''', demandas)

    conn.commit()
    conn.close()
    print("Datos de prueba insertados correctamente.")
    

def obtener_input_valido(mensaje: str, tipo_dato: type, mensaje_error: str) -> Optional[Union[str, int, float]]:
    while True:
        entrada = input(mensaje).strip()
        if entrada == '0':
            print("Operación cancelada.")
            return None
        if tipo_dato == str:
            return entrada
        elif tipo_dato == int:
            try:
                return int(entrada)
            except ValueError:
                print(mensaje_error)
        elif tipo_dato == float:
            try:
                return float(entrada)
            except ValueError:
                print(mensaje_error)

def agregar_proveedor(cursor):
    nombre_proveedor = obtener_input_valido("Ingrese el nombre del proveedor: ", str, "Por favor ingrese un nombre válido.")
    if nombre_proveedor is None: return None
    contacto = obtener_input_valido("Ingrese el contacto del proveedor: ", str, "Por favor ingrese un contacto válido.")
    if contacto is None: return None
    telefono = obtener_input_valido("Ingrese el teléfono del proveedor: ", str, "Por favor ingrese un teléfono válido.")
    if telefono is None: return None
    email = obtener_input_valido("Ingrese el email del proveedor: ", str, "Por favor ingrese un email válido.")
    if email is None: return None
    pais = obtener_input_valido("Ingrese el país del proveedor: ", str, "Por favor ingrese un país válido.")
    if pais is None: return None
    tiempo_entrega = obtener_input_valido("Ingrese el tiempo de entrega (días): ", int, "Por favor ingrese un tiempo válido.")
    if tiempo_entrega is None: return None

    cursor.execute('''INSERT INTO Proveedores (nombre_proveedor, contacto, telefono, email, pais, tiempo_entrega)  
                    VALUES (?, ?, ?, ?, ?, ?)''', (nombre_proveedor, contacto, telefono, email, pais, tiempo_entrega))
    return cursor.lastrowid

def seleccionar_proveedor() -> Optional[int]:
    conn = crear_conexion()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM Proveedores")
        proveedores = cursor.fetchall()

        if proveedores:
            df_proveedores = pd.DataFrame(proveedores, columns=["ID Proveedor", "Nombre", "Contacto", "Teléfono", "Email", "País", "Tiempo de Entrega (días)"])
            print("\nLista de Proveedores:")
            print(tabulate(df_proveedores, headers='keys', tablefmt='fancy_grid', showindex=False))
        else:
            print("No hay proveedores registrados.")
            return None

        seleccion = obtener_input_valido("\nIngrese el ID del proveedor que desea seleccionar o escriba '//' para agregar uno nuevo: ", str, "Selección no válida.")
        if seleccion is None or seleccion == '0':  # Asegurarse de que seleccion no sea None ni '0'
            print("Operación cancelada.")
            return None
        if seleccion == '//':
            proveedor_id = agregar_proveedor(cursor)
            conn.commit()
            if proveedor_id:
                print("Proveedor agregado correctamente.")
                return proveedor_id
            return None
        else:
            try:
                id_proveedor = int(seleccion)
                cursor.execute("SELECT * FROM Proveedores WHERE id_proveedor = ?", (id_proveedor,))
                proveedor = cursor.fetchone()
                if proveedor:
                    return id_proveedor
                else:
                    print("Proveedor no encontrado.")
                    return None
            except ValueError:
                print("Selección no válida. No se seleccionará ningún proveedor.")
                return None
    finally:
        conn.close()


def insertar_producto():
    print("\n--- Ingresar Producto ---")
    
    conn = crear_conexion()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM Proveedores")
    proveedores_existen = cursor.fetchone()[0] > 0
    
    if not proveedores_existen:
        print("No hay proveedores disponibles. Por favor, agregue un proveedor.")
        proveedor_id = agregar_proveedor(cursor) 
        conn.commit()
        if proveedor_id:
            print("Proveedor agregado correctamente.")
        else:
            print("No se pudo agregar el proveedor.")
            conn.close()
            return  
    conn.close()
    
    proveedor_id = seleccionar_proveedor()
    if proveedor_id is None: return

    conn = crear_conexion()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Proveedores WHERE id_proveedor = ?", (proveedor_id,))
    proveedor = cursor.fetchone()

    if proveedor:
        nombre_producto = obtener_input_valido("Ingrese el nombre del producto: ", str, "Por favor ingrese un nombre válido.")
        if nombre_producto is None: return
        
        demanda_diaria = obtener_input_valido("Ingrese la demanda diaria: ", int, "Por favor ingrese una demanda válida.")
        if demanda_diaria is None: return
        
        tiempo_entrega = proveedor[6]
        stock_seguridad = obtener_input_valido("Ingrese el stock de seguridad: ", int, "Por favor ingrese un stock válido.")
        if stock_seguridad is None: return
        
        precio = obtener_input_valido("Ingrese el precio del producto: ", float, "Por favor ingrese un precio válido.")
        if precio is None: return

        cursor.execute('''INSERT INTO Productos (nombre_producto, stock_seguridad, precio, proveedor_id)  
                        VALUES (?, ?, ?, ?)''', (nombre_producto, stock_seguridad, precio, proveedor_id))

        conn.commit()
        print("Producto agregado correctamente.")
        
        demanda_mensual = demanda_diaria * 30  
        
        cursor.execute('''INSERT INTO Demanda_Promedio (id_producto, demanda_diaria, demanda_mensual, fecha_registro)
                        VALUES ((SELECT id_producto FROM Productos WHERE nombre_producto = ?), ?, ?, ?)''',
                       (nombre_producto, demanda_diaria, demanda_mensual, datetime.now().strftime('%Y-%m-%d')))
        
        conn.commit()

        valor_anual = precio * demanda_mensual * 12
        valor_total = calcular_valor_total()  
        limite_a = valor_total * 0.8
        limite_b = valor_total * 0.95
        
        if valor_anual <= limite_a:
            clasificacion = 'A'
        elif valor_anual <= limite_b:
            clasificacion = 'B'
        else:
            clasificacion = 'C'

        cursor.execute('''UPDATE Productos SET clasificacion_abc = ? 
                          WHERE id_producto = (SELECT id_producto FROM Productos WHERE nombre_producto = ?)''',
                       (clasificacion, nombre_producto))

        conn.commit()
    else:
        print("No se encontró información para este proveedor.")

    conn.close()


def calcular_valor_total():
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT SUM(P.precio * D.demanda_mensual * 12)
        FROM Productos P
        JOIN Demanda_Promedio D ON P.id_producto = D.id_producto
    ''')
    valor_total = cursor.fetchone()[0] or 0  # Evitar None si no hay productos
    conn.close()
    return valor_total

def insertar_pedido():
    print("\n--- Ingresar Pedido ---")
    
    conn = crear_conexion()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Proveedores")
    proveedores = cursor.fetchall()

    if not proveedores:
        print("No hay proveedores registrados.")
        conn.close()
        return

    df_proveedores = pd.DataFrame(proveedores, columns=["ID Proveedor", "Nombre", "Contacto", "Teléfono", "Email", "País", "Tiempo de Entrega (días)"])
    print("\nProveedores disponibles:")
    print(tabulate(df_proveedores, headers='keys', tablefmt='fancy_grid', showindex=False))

    proveedor_id = obtener_input_valido("Ingrese el ID del proveedor al que desea pedir: ", int, "Por favor ingrese un ID válido.")
    if proveedor_id not in df_proveedores['ID Proveedor'].values:
        print("Proveedor no encontrado. Operación cancelada.")
        conn.close()
        return

    cursor.execute('''
        SELECT Pr.id_producto, Pr.nombre_producto 
        FROM Productos Pr
        WHERE Pr.proveedor_id = ?
    ''', (proveedor_id,))
    productos_proveedor = cursor.fetchall()

    if not productos_proveedor:
        print("No hay productos asociados a este proveedor.")
        conn.close()
        return

    df_productos_proveedor = pd.DataFrame(productos_proveedor, columns=["ID Producto", "Nombre Producto"])
    print("\nProductos disponibles del proveedor seleccionado:")
    print(tabulate(df_productos_proveedor, headers='keys', tablefmt='fancy_grid', showindex=False))

    producto_id = obtener_input_valido("Ingrese el ID del producto que desea seleccionar: ", int, "Por favor ingrese un ID válido.")
    if producto_id not in df_productos_proveedor['ID Producto'].values:
        print("Producto no encontrado. Operación cancelada.")
        conn.close()
        return

    cantidad_pedida = obtener_input_valido("Ingrese la cantidad que desea pedir: ", int, "Por favor ingrese una cantidad válida.")
    fecha_pedido = datetime.now()
    fecha_entrega = fecha_pedido + timedelta(days=5)

    fecha_pedido_str = fecha_pedido.strftime('%Y-%m-%d')
    fecha_entrega_str = fecha_entrega.strftime('%Y-%m-%d')

    cursor.execute('''INSERT INTO Pedidos (id_producto, cantidad_pedida, fecha_pedido, fecha_entrega, estado_pedido)  
                    VALUES (?, ?, ?, ?, ?)''', (producto_id, cantidad_pedida, fecha_pedido_str, fecha_entrega_str, 'Pendiente'))

    conn.commit()
    conn.close()
    print("Pedido agregado correctamente.")

def actualizar_inventario():
    print("\n--- Actualizar Inventario en Base a Pedidos ---")
    
    conn = crear_conexion()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT Pe.id_pedido, Pe.id_producto, Pr.nombre_producto, Pe.cantidad_pedida, Pe.fecha_pedido, Pe.fecha_entrega, Pe.estado_pedido 
        FROM Pedidos Pe
        JOIN Productos Pr ON Pe.id_producto = Pr.id_producto
        WHERE Pe.estado_pedido = 'Pendiente'
    ''')
    pedidos = cursor.fetchall()

    if not pedidos:
        print("No hay pedidos pendientes para actualizar el inventario.")
        conn.close()
        return

    df_pedidos = pd.DataFrame(pedidos, columns=["ID Pedido", "ID Producto", "Nombre Producto", "Cantidad Pedida", "Fecha Pedido", "Fecha Entrega", "Estado"])
    print("\nPedidos Pendientes:")
    print(tabulate(df_pedidos, headers='keys', tablefmt='fancy_grid', showindex=False))

    id_pedido = obtener_input_valido("Ingrese el ID del pedido que desea confirmar: ", int, "Por favor ingrese un ID válido.")

    cursor.execute("SELECT * FROM Pedidos WHERE id_pedido = ? AND estado_pedido = 'Pendiente'", (id_pedido,))
    pedido = cursor.fetchone()

    if not pedido:
        print("Pedido no encontrado o ya fue actualizado.")
        conn.close()
        return

    id_producto, cantidad_pedida = pedido[1], pedido[2]

    cursor.execute("UPDATE Productos SET stock_actual = stock_actual + ? WHERE id_producto = ?", (cantidad_pedida, id_producto))

    cursor.execute("UPDATE Pedidos SET estado_pedido = 'Completado' WHERE id_pedido = ?", (id_pedido,))

    fecha_movimiento = datetime.now().date()
    cursor.execute('''INSERT INTO Historial_Inventario (id_producto, cantidad, tipo_movimiento, fecha_movimiento, razon)
                    VALUES (?, ?, ?, ?, ?)''', (id_producto, cantidad_pedida, "Entrada", fecha_movimiento, "Pedido recibido"))

    conn.commit()
    conn.close()
    print("Inventario actualizado correctamente con el pedido seleccionado.")


def mostrar_historial_inventario():
    try:
        conn = crear_conexion()
        cursor = conn.cursor()

        cursor.execute('''SELECT P.id_producto, P.nombre_producto, Pr.nombre_proveedor 
                          FROM Productos P
                          JOIN Proveedores Pr ON P.proveedor_id = Pr.id_proveedor''')
        productos = cursor.fetchall()

        if productos:
            df_productos = pd.DataFrame(productos, columns=["ID Producto", "Nombre Producto", "Proveedor"])
            print("\nLista de Productos y Proveedores:")
            print(tabulate(df_productos, headers='keys', tablefmt='fancy_grid', showindex=False))
        else:
            print("No hay productos registrados.")
            conn.close()
            return

        id_producto = obtener_input_valido("Ingrese el ID del producto para mostrar el historial: ", int, "Por favor ingrese un ID válido.")

        cursor.execute('''SELECT * FROM Historial_Inventario WHERE id_producto = ? ORDER BY fecha_movimiento DESC''', (id_producto,))
        historial = cursor.fetchall()

        if historial:
            df_historial = pd.DataFrame(historial, columns=["ID Historial", "ID Producto", "Cantidad", "Tipo Movimiento", "Fecha Movimiento", "Razón"])
            print("\nHistorial de Movimientos:")
            print(tabulate(df_historial, headers='keys', tablefmt='fancy_grid', showindex=False))
        else:
            print("No hay movimientos registrados para este producto.")

        conn.close()
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")
        conn.close()

def verificar_reorden():
    try:
        print("\n--- Verificación de Punto de Reorden ---")
        
        conn = crear_conexion()
        cursor = conn.cursor()

        cursor.execute('''SELECT id_producto, nombre_producto, stock_actual, punto_reorden
                          FROM Productos
                          WHERE stock_actual <= punto_reorden''')
        productos_para_reorden = cursor.fetchall()

        if productos_para_reorden:
            print("\nProductos que necesitan reordenarse:")
            df_productos = pd.DataFrame(productos_para_reorden, columns=["ID Producto", "Nombre Producto", "Stock Actual", "Punto de Reorden"])
            print(tabulate(df_productos, headers='keys', tablefmt='fancy_grid', showindex=False))

            id_producto_seleccionado = obtener_input_valido("Seleccione el ID del producto que desea reordenar: ", int, "Por favor ingrese un ID válido.")
            if id_producto_seleccionado is None:
                return

            producto_encontrado = next((p for p in productos_para_reorden if p[0] == id_producto_seleccionado), None)

            if producto_encontrado:
                id_producto, nombre_producto, stock_actual, punto_reorden = producto_encontrado
                cantidad_necesaria = punto_reorden - stock_actual + 1

                print("Reorden hecho correctamente")

                nuevo_stock = stock_actual + cantidad_necesaria
                cursor.execute('''UPDATE Productos
                                  SET stock_actual = ?
                                  WHERE id_producto = ?''', (nuevo_stock, id_producto_seleccionado))

                conn.commit()
                print(f"El stock del producto '{nombre_producto}' ha sido actualizado a {nuevo_stock} unidades.")

            else:
                print("El ID seleccionado no corresponde a un producto en la lista.")
        else:
            print("Todos los productos están por encima de su punto de reorden.")

        conn.close()
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")
        conn.close()



def clasificacion_abc():
    print("\n--- Clasificación ABC ---")
    
    try:
        conn = crear_conexion()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT Pr.id_producto, Pr.nombre_producto, Pr.precio, Dm.demanda_mensual
            FROM Productos Pr
            JOIN Demanda_Promedio Dm ON Pr.id_producto = Dm.id_producto
        ''')
        productos = cursor.fetchall()

        if not productos:
            print("No hay productos ni demanda registrada para realizar la clasificación ABC.")
            return

        productos_abc = []
        for id_producto, nombre_producto, precio, demanda_mensual in productos:
            valor_anual = precio * demanda_mensual * 12
            productos_abc.append((id_producto, nombre_producto, valor_anual))

        productos_abc.sort(key=lambda x: x[2], reverse=True)

        valor_total = sum([valor for _, _, valor in productos_abc])
        limite_a = valor_total * 0.8
        limite_b = valor_total * 0.95

        clasificacion = []
        valor_acumulado = 0
        for id_producto, nombre_producto, valor_anual in productos_abc:
            valor_acumulado += valor_anual
            if valor_acumulado <= limite_a:
                categoria = 'A'
            elif valor_acumulado <= limite_b:
                categoria = 'B'
            else:
                categoria = 'C'
            clasificacion.append((id_producto, nombre_producto, valor_anual, categoria))

        df_clasificacion = pd.DataFrame(clasificacion, columns=["ID Producto", "Nombre Producto", "Valor Anual", "Categoría"])
        print(tabulate(df_clasificacion, headers='keys', tablefmt='fancy_grid', showindex=False))

    except Exception as e:
        print(f"Ocurrió un error al realizar la clasificación ABC: {e}")

    finally:
        if conn:
            conn.close()


def seleccionar_producto():
    conn = crear_conexion()
    cursor = conn.cursor()

    cursor.execute("SELECT id_producto, nombre_producto, precio, stock_actual, stock_seguridad, punto_reorden, proveedor_id FROM Productos")
    productos = cursor.fetchall()

    if productos:
        df_productos = pd.DataFrame(productos, columns=["ID Producto", "Nombre Producto", "Precio", "Stock Actual", "Stock Seguridad", "Punto de Reorden", "ID Proveedor"])
        print("\nLista de Productos:")
        print(tabulate(df_productos, headers='keys', tablefmt='fancy_grid', showindex=False))
    else:
        print("No hay productos registrados.")
        return None

    seleccion = obtener_input_valido("Ingrese el ID del producto que desea seleccionar: ", int, "Por favor ingrese un ID válido.")
    if seleccion is not None:
        cursor.execute("SELECT * FROM Productos WHERE id_producto = ?", (seleccion,))
        producto = cursor.fetchone()
        if producto:
            return seleccion
        else:
            print("Producto no encontrado.")
            return None
    return None

def calcular_eoq(demanda_anual, costo_pedido, costo_almacenamiento):
    if demanda_anual > 0 and costo_pedido > 0 and costo_almacenamiento > 0:
        return round(((2 * demanda_anual * costo_pedido) / costo_almacenamiento) ** 0.5)
    return 0

def EOQ():
    print("\n--- Determinar EOQ ---")
    
    try:
        conn = crear_conexion()
        cursor = conn.cursor()

        cursor.execute('''SELECT Pr.nombre_producto, Dm.demanda_mensual, Pr.costo_pedido, Pr.costo_almacenamiento
                          FROM Productos Pr
                          JOIN Demanda_Promedio Dm ON Pr.id_producto = Dm.id_producto''')
        productos = cursor.fetchall()

        tabla_datos = []
        for producto in productos:
            nombre_producto, demanda_mensual, costo_pedido, costo_almacenamiento = producto
            
            demanda_anual = demanda_mensual * 12
            eoq = calcular_eoq(demanda_anual, costo_pedido, costo_almacenamiento)
            
            if eoq is not None:
                tabla_datos.append([nombre_producto, demanda_anual, costo_pedido, costo_almacenamiento, f"{eoq:.2f}"])
        
        cabecera = ["Producto", "Demanda Anual", "Costo Pedido", "Costo Almacenamiento", "EOQ Calculado"]
        
        print(tabulate(tabla_datos, headers=cabecera, tablefmt="fancy_grid"))

    except Exception as e:
        print(f"Ocurrió un error al calcular el EOQ: {e}")

    finally:
        if conn:
            conn.close()


def adaptador_fecha(fecha):
    return fecha.strftime('%Y-%m-%d')


def reporte_todos_los_productos():
    print("\n--- Generar Reporte Completo de Todos los Productos ---")
    
    try:
        conn = crear_conexion()
        cursor = conn.cursor()

        cursor.execute('''SELECT P.id_producto, P.nombre_producto, P.precio, P.stock_actual, P.stock_seguridad, Pr.nombre_proveedor
                          FROM Productos P
                          JOIN Proveedores Pr ON P.proveedor_id = Pr.id_proveedor''')
        productos = cursor.fetchall()

        if not productos:
            print("No hay productos en la base de datos.")
            conn.close()
            return
        
        cursor.execute('''SELECT Dm.id_producto, Dm.demanda_diaria, Dm.demanda_mensual FROM Demanda_Promedio Dm''')
        demanda = cursor.fetchall()
        demanda_dict = {d[0]: (d[1], d[2]) for d in demanda}

        cursor.execute('''SELECT id_producto, costo_pedido, costo_almacenamiento FROM Productos''')
        costos = cursor.fetchall()
        costos_dict = {c[0]: (c[1], c[2]) for c in costos}

        reporte = []

        for producto in productos:
            producto_id = producto[0]
            nombre_producto = producto[1]
            precio = producto[2]
            stock_actual = producto[3]
            stock_seguridad = producto[4]
            proveedor = producto[5]

            demanda_diaria, demanda_mensual = demanda_dict.get(producto_id, (0, 0))

            demanda_anual = demanda_mensual * 12
            valor_anual = precio * demanda_anual
            categoria_abc = 'A' if valor_anual >= 100000 else 'B' if valor_anual >= 50000 else 'C'

            costo_pedido, costo_mantener = costos_dict.get(producto_id, (0, 0))

            eoq = calcular_eoq(demanda_anual, costo_pedido, costo_mantener) if demanda_anual > 0 else 0

            plazo_entrega = 7
            punto_reorden_calculado = demanda_diaria * plazo_entrega
            necesita_reorden = "Sí" if stock_actual < punto_reorden_calculado else "No"

            reporte.append([producto_id, nombre_producto, precio, stock_actual, stock_seguridad, proveedor,
                            round(demanda_diaria, 2), round(demanda_mensual, 2), round(valor_anual), categoria_abc,
                            round(eoq), round(punto_reorden_calculado), necesita_reorden])

        columnas = ["ID Producto", "Nombre Producto", "Precio", "Stock Actual", "Stock Seguridad", "Proveedor",
                    "Demanda Diaria", "Demanda Mensual", "Valor Anual", "Clasificación ABC", "EOQ", "Punto de Reorden",
                    "¿Necesita Reorden?"]

        df_reporte = pd.DataFrame(reporte, columns=columnas)

        print(tabulate(df_reporte, headers='keys', tablefmt='fancy_grid', showindex=False))

    except Exception as e:
        print(f"Ocurrió un error al generar el reporte: {e}")
    
    finally:
        if conn:
            conn.close()






def menu_principal():
    while True:
        print("\nMenu Principal:")
        print("1. Agregar nuevo producto")
        print("2. Agregar nuevo pedido")
        print("3. Actualizar inventario")
        print("4. Mostrar historial de inventario")
        print("5. Verificar punto de reorden")
        print("6. Clasificación ABC")
        print("7. Determinar EOQ")
        print("8. REPORTE LABORAL")
        print("9. Salir")

        opcion = obtener_input_valido("Seleccione una opción: ", int, "Por favor ingrese una opción válida.")

        if opcion == 1:
            insertar_producto()
        elif opcion == 2:
            insertar_pedido()
        elif opcion == 3:
            actualizar_inventario()
        elif opcion == 4:
            mostrar_historial_inventario()
        elif opcion == 5:
            verificar_reorden()
        elif opcion == 6:
            clasificacion_abc()
        elif opcion == 7:
            EOQ()
        elif opcion == 8:
            reporte_todos_los_productos()
        elif opcion == 9:   
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")


if __name__ == "__main__":
    crear_tablas()
    insertar_datos_prueba()
    menu_principal()

    
#Script adicional que se puede usar en otro archivo en la misma carpeta para hacer pruebas en el codigo
"""
import sqlite3
import random
from datetime import datetime, timedelta

# Adaptador para fechas (evitar el warning en versiones de Python 3.12+)
def adaptador_fecha(fecha):
    return fecha.strftime('%Y-%m-%d')  # Formato YYYY-MM-DD

def crear_conexion() -> sqlite3.Connection:
    try:
        conn = sqlite3.connect('inventario.db')
        sqlite3.register_adapter(datetime, adaptador_fecha)  # Registrar adaptador para fechas
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        raise

def insertar_datos_prueba():
    conn = crear_conexion()
    cursor = conn.cursor()

    # Insertar Proveedores de prueba (50 proveedores)
    proveedores = []
    for i in range(1, 51):
        proveedores.append((
            f'Proveedor {i}',
            f'Contacto {i}',
            f'555-1{i}23{i}',
            f'contacto{i}@proveedor{i}.com',
            random.choice(['México', 'Estados Unidos', 'Canadá', 'Argentina', 'Colombia']),
            random.randint(1, 10)
        ))

    cursor.executemany('''INSERT INTO Proveedores (nombre_proveedor, contacto, telefono, email, pais, tiempo_entrega)  
                        VALUES (?, ?, ?, ?, ?, ?)''', proveedores)

    # Insertar Productos de prueba (50 productos)
    productos = []
    for i in range(1, 51):
        productos.append((
            f'Producto {i} Clásico',
            round(random.uniform(40.0, 100.0), 2),  # Precio aleatorio entre 40 y 100
            random.randint(5, 20),  # Stock actual aleatorio entre 5 y 20
            random.randint(2, 10),  # Stock de seguridad aleatorio entre 2 y 10
            random.randint(10, 20),  # Punto de reorden aleatorio entre 10 y 20
            random.randint(1, 50),  # ID de proveedor aleatorio
            random.choice(['A', 'B', 'C']),  # Clasificación ABC aleatoria
            random.randint(10, 30)  # EOQ aleatorio entre 10 y 30
        ))

    cursor.executemany('''INSERT INTO Productos (nombre_producto, precio, stock_actual, stock_seguridad, punto_reorden, proveedor_id, clasificacion_abc, eoq)  
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', productos)

    # Insertar Pedidos de prueba (50 pedidos)
    pedidos = []
    for _ in range(50):
        id_producto = random.randint(1, 50)  # Producto aleatorio
        cantidad_pedida = random.randint(1, 10)  # Cantidad aleatoria entre 1 y 10
        fecha_pedido = datetime.now().date()
        fecha_entrega = fecha_pedido + timedelta(days=random.randint(1, 7))  # Fecha de entrega aleatoria entre 1 y 7 días
        estado_pedido = random.choice(['Pendiente', 'Enviado', 'Entregado'])  # Estado aleatorio

        pedidos.append((id_producto, cantidad_pedida, fecha_pedido, fecha_entrega, estado_pedido))

    cursor.executemany('''INSERT INTO Pedidos (id_producto, cantidad_pedida, fecha_pedido, fecha_entrega, estado_pedido)  
                        VALUES (?, ?, ?, ?, ?)''', pedidos)

    # Insertar Historial de Inventario de prueba (50 registros)
    historial_inventario = []
    for _ in range(50):
        id_producto = random.randint(1, 50)  # Producto aleatorio
        cantidad = random.randint(1, 10)  # Cantidad de movimiento aleatoria entre 1 y 10
        tipo_movimiento = random.choice(['Entrada', 'Salida'])  # Movimiento aleatorio (entrada o salida)
        fecha_movimiento = datetime.now().date()
        razon = random.choice(['Compra', 'Venta', 'Devolución', 'Ajuste'])  # Razón aleatoria

        historial_inventario.append((id_producto, cantidad, tipo_movimiento, fecha_movimiento, razon))

    cursor.executemany('''INSERT INTO Historial_Inventario (id_producto, cantidad, tipo_movimiento, fecha_movimiento, razon)  
                        VALUES (?, ?, ?, ?, ?)''', historial_inventario)

    # Insertar Demanda Promedio de prueba (50 registros de demanda)
    demandas = []
    for i in range(1, 51):
        demandas.append((
            i,  # ID del producto
            random.randint(1, 10),  # Demanda diaria aleatoria entre 1 y 10
            random.randint(30, 300),  # Demanda mensual aleatoria entre 30 y 300
            datetime.now().date()  # Fecha actual
        ))

    cursor.executemany('''INSERT INTO Demanda_Promedio (id_producto, demanda_diaria, demanda_mensual, fecha_registro)  
                        VALUES (?, ?, ?, ?)''', demandas)

    # Confirmar los cambios e insertar los datos
    conn.commit()
    conn.close()
    print("Datos de prueba insertados correctamente.")

if __name__ == "__main__":
    insertar_datos_prueba()

"""