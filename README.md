# Servicio-Web-SOAP
Este proyecto implementa un servicio web SOAP utilizando Python y la biblioteca Spyne, que permite realizar operaciones CRUD (Crear, Consultar, Actualizar y Eliminar) sobre una base de datos MySQL.
📌 Métodos disponibles

insertarProducto(nombre, descripcion, precio, stock)

Agrega un nuevo producto a la base de datos.

consultarProducto(id)

Obtiene los detalles de un producto específico mediante su ID.

actualizarProducto(id, nombre, descripcion, precio, stock)

Modifica la información de un producto existente.

eliminarProducto(id)

Elimina un producto según su ID.

🚀 Cómo funciona el código
Conexión a MySQL
La función get_connection() se encarga de establecer la conexión con la base de datos MySQL, utilizando el usuario root sin contraseña y la base de datos tienda.

Servicio SOAP (ProductoService)
Se define una clase heredada de ServiceBase con métodos decorados con @rpc, los cuales representan las operaciones expuestas por el servicio.

Operaciones CRUD
Cada método accede a la base de datos mediante mysql.connector, ejecuta la consulta correspondiente (INSERT, SELECT, UPDATE, DELETE), y retorna un mensaje indicando el resultado.

Aplicación SOAP
La clase Application define el endpoint SOAP, incluyendo el protocolo (Soap11), el espacio de nombres (tns) y la validación de entrada con lxml.

Servidor local
Se lanza un servidor WSGI simple en localhost:8000, donde puedes acceder al WSDL desde:
👉 http://localhost:8000/?wsdl

Puedes probarlo con SoapUI, importando el wsdl y después ya puedes crear peticiones a los metodos definidos.
