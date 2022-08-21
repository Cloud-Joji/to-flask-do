import os

from flask import Flask

def create_app():
  app = Flask(__name__)
  
  # From Mapping nos va a permitir definir variables de configuracion que utilizaremos en la app 
  app.config.from_mapping(
    # Es una llave para definir las sesiones en la aplicacion, en este caso seria la cookie que se le envia al usuario para que tenga
    # un uid de sesion para saber quien es el usuario que esta haciendo la peticion, el string tiene que ser complicado en produccion
    # para que no roben la informacion
    SECRET_KEY='mykey',
    # Define la base de datos host, donde nos queremos conectar, sacamos los valores de variables de entorno
    DATABASE_HOST=os.environ.get('FLASK_DATABASE_HOST'),
    # Define el usuario que va a conectarse a la base de datos
    DATABASE_USER=os.environ.get('FLASK_DATABASE_USER'),
    # Define la contraseña del usuario que va a conectarse a la base de datos
    DATABASE_PASSWORD=os.environ.get('FLASK_DATABASE_PASSWORD'),
    # Define el nombre de la base de datos que va a conectarset
    DATABASE=os.environ.get('FLASK_DATABASE'),
  )

  @app.route('/hello')
  def hello():
    return 'Hello World!'

  return app