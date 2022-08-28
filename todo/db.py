# Importa MYSQL Connector
import mysql.connector
# Importa click, sirve para ejecutar comandos en el terminal
# Con el podemos crear tablas, relacion entre ellos a traves de
# Comandos sin tener que ingresar a MYSql workbench
import click

# current_app mantiene la aplicacion que estamos ejecutando
# g utlizaremos para almacenar al usuario
from flask import current_app, g
# with_appcontext nos va a servir cuando ejecutemos el script de base de datos
# ya que vamos a necesitar el contexto de la configuracion de la aplicacion
# cuando ejecutamos el escript con appcontext podemos acceder a las variables
# que se encuentra en la configuracion de la aplicacion, como el host, usuario y pass
from flask.cli import with_appcontext
# Va a contener todos los scripts que necesitamos para crear la base de datos
from .schema import instructions

# Funcion que nos va a permitir obtener la base de datos y tambien
# el cursor dentro de la app


def get_db():
    # Si no se encuentra el atributo db dentro de g
    if 'db' not in g:
        # Creamos nueva propiedad dentro de G que va a contener la conexion a la BD
        g.db = mysql.connector.connect(
            host=current_app.config['DATABASE_HOST'],
            user=current_app.config['DATABASE_USER'],
            password=current_app.config['DATABASE_PASSWORD'],
            database=current_app.config['DATABASE']
        )
    # Definimos dentro de g la propiedad de c
    # Queremos acceder a las propiedades como un diccionario,
    # debemos pasar la propuiedad de dictionary dentro de cursor como true
        g.c = g.db.cursor(dictionary=True)
# cuando llamemos a get_db obtendremos el base de datos y el cursor
    return g.db, g.c

# Funcion para cerrar la base de datos que ejecutaremos para cerrar la base de datos
# El cual le indicaremos a flask que cierre la conexion al a base de datos
# al finalizar una operacoin


def close_db(e=None):
    # Llamamos a db para quitarle la propiedad db a g
    db = g.pop('db', None)
    # Si db no se encuentra definido significa que nunca llamamos a get_db
    # si db se encuentra definido se cerrara la base de datos
    if db is not None:
        db.close()


def init_db():
    db, c = get_db()

    for i in instructions:
        c.execute(i)

    db.commit()

# Define nombre para utilizarlo por consola


@click.command('init-db')
# Para que se ejecute con exito, que utilice el contexto de la app
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Base de datos inicializada!')

# Funcion que le pasamos como argumento app
# Que se ejecutara cuando finalice el contexto de la app
# Cuando termine de ejecutar una peticion cierra la conexion


def init_app(app):
    app.cli.add_command(init_db_command)
    app.teardown_appcontext(close_db)
