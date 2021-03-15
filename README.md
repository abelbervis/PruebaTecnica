# Prueba Tecnica

_proyecto de prueba aplicacion de ventas,facturacion e inventario_


### Pre-requisitos 📋


### Instalación 🔧

_Para correr la aplicación se necesita tener todos los requerimientos instalados y una base de datos postgreSQL con los datos que están en config._

```
pip install –r requirements/requirements.txt
```
_el nombre de la BD postgreSQL y su validacion se encuentran en config->db del proyecto_
```
POSTGRESQL = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'prueba',
        'USER': 'postgres',
        'PASSWORD': 'tucontrasena',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}
```

_Luego que tenemos la bd creada hay que hacer las migraciones de la bd_

```
python manage.py makemigrations
```
```
python manage.py migrate
```
_Crear un superusuario para acceder a la aplicacion_

```
python manage.py createsuperuser
```
_luego agregamos las credenciales de ese usuario y asi poder acceder al login_


## Construido con 🛠️

* Django 3.0.7 
* Python 3.7.4
* PostgresSQL 13 
* PyCharm 2020.2.3


## Autores ✒️

* **Abel Bervis** 


## Expresiones de Gratitud 🎁

* Muchas gracias por el tomarse el tiempo de revisar este proyecto

