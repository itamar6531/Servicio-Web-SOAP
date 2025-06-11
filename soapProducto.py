from spyne import Application, rpc, ServiceBase, Integer, Unicode, Decimal, Float
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import mysql.connector
from wsgiref.simple_server import make_server

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="", 
        database="tienda"
    )

class ProductoService(ServiceBase):

    @rpc(Unicode, Unicode, Decimal, Integer, _returns=Unicode)
    def insertarProducto(ctx, nombre, descripcion, precio, stock):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            sql = "INSERT INTO productos (nombre, descripcion, precio, stock) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (nombre, descripcion, float(precio), stock))
            conn.commit()
            return "Producto insertado correctamente"
        except Exception as e:
            return f"Error al insertar: {str(e)}"
        finally:
            cursor.close()
            conn.close()

    @rpc(Integer, _returns=Unicode)
    def consultarProducto(ctx, id):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM productos WHERE id = %s", (id,))
            result = cursor.fetchone()
            if result:
                return str(result)
            else:
                return "Producto no encontrado"
        except Exception as e:
            return f"Error al consultar: {str(e)}"
        finally:
            cursor.close()
            conn.close()

    @rpc(Integer, Unicode, Unicode, Decimal, Integer, _returns=Unicode)
    def actualizarProducto(ctx, id, nombre, descripcion, precio, stock):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            sql = "UPDATE productos SET nombre = %s, descripcion = %s, precio = %s, stock = %s WHERE id = %s"
            cursor.execute(sql, (nombre, descripcion, float(precio), stock, id))
            conn.commit()
            if cursor.rowcount > 0:
                return "Producto actualizado correctamente"
            else:
                return "Producto no encontrado"
        except Exception as e:
            return f"Error al actualizar: {str(e)}"
        finally:
            cursor.close()
            conn.close()

    @rpc(Integer, _returns=Unicode)
    def eliminarProducto(ctx, id):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
            conn.commit()
            if cursor.rowcount > 0:
                return "Producto eliminado correctamente"
            else:
                return "Producto no encontrado"
        except Exception as e:
            return f"Error al eliminar: {str(e)}"
        finally:
            cursor.close()
            conn.close()

application = Application(
    [ProductoService],
    tns='http://localhost:8000/producto',  # <- usa una URL como target namespace
    name='ProductoService',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_app = WsgiApplication(application)

if __name__ == '__main__':
    print("Servicio SOAP disponible en http://localhost:8000/?wsdl")
    server = make_server('0.0.0.0', 8000, wsgi_app)
    server.serve_forever()
