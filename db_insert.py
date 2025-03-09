import sqlite3
import random
from datetime import datetime, timedelta

# Función para crear la conexión a la base de datos
def crear_conexion() -> sqlite3.Connection:
    try:
        conn = sqlite3.connect('inventario.db')
        sqlite3.register_adapter(datetime, adaptador_fecha)  # Registrar adaptador para fechas
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        raise

# Adaptador para fechas (evitar el warning en versiones de Python 3.12+)
def adaptador_fecha(fecha):
    return fecha.strftime('%Y-%m-%d')  # Formato YYYY-MM-DD

# Función para crear las tablas sin cálculos de ABC, demanda, EOQ o punto de reorden
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

    # Insertar Productos de cristal de prueba (50 productos)
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
        costo_pedido = round(random.uniform(5.0, 20.0), 2)  # Costo de pedido aleatorio entre 5 y 20
        costo_almacenamiento = round(random.uniform(1.0, 5.0), 2)  # Costo de almacenamiento aleatorio entre 1 y 5
        productos.append((
            nombre_producto,
            round(random.uniform(40.0, 100.0), 2),  # Precio aleatorio entre 40 y 100
            random.randint(5, 20),  # Stock actual aleatorio entre 5 y 20
            random.randint(2, 10),  # Stock de seguridad aleatorio entre 2 y 10
            random.randint(10, 20),  # Punto de reorden aleatorio entre 10 y 20
            random.randint(1, 50),  # ID de proveedor aleatorio
            random.choice(['A', 'B', 'C']),  # Clasificación ABC aleatoria
            random.randint(10, 30),  # EOQ aleatorio entre 10 y 30
            costo_pedido,  # Costo de pedido
            costo_almacenamiento  # Costo de almacenamiento
        ))

    cursor.executemany('''INSERT INTO Productos (nombre_producto, precio, stock_actual, stock_seguridad, punto_reorden, proveedor_id, clasificacion_abc, eoq, costo_pedido, costo_almacenamiento)  
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', productos)

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
    crear_tablas()  # Crear las tablas antes de insertar los datos
    insertar_datos_prueba()  # Insertar datos de prueba
