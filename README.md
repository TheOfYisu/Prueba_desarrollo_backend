# Prueba_desarrollo_backend

Para ejecutarlo tiene que tener instalado python.

Ya una vez instalado se tiene que instalar Connector de MySQL parra Python.

    https://dev.mysql.com/downloads/connector/python/

Ya una vez instalado el Connectorr de MySQL, se tendran que instalar las siguientes librerias.

Librería de JWT

    pip install pyjwt

Librería de Flask
  
    pip install flask

Librería de Cors

    pip install flask-cors


Librería de Peewee
-- Se usa para ORM (Mapeo Objeto-Relacional)

    pip install peewee

Adicional se instala otro conector de MySQL

    pip install mysql-connector-python


En caso de dar error de puerto en la ejecucion, al final se podra camiar el puerto a utilizar.

    app.run(port=5500, debug=True)