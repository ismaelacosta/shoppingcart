from flask import Flask
#from sqlalchemy.orm import session
#Localizar las direcciones en otras rutas
from api.routes.carrito_routes import carrito_blueprint

from api.utils.db import Session


app = Flask(__name__)

#Guarda transacciones en la base de datos, sin embargo no utilizamos esta forma para manejarlo
#session = Session()

app.register_blueprint(carrito_blueprint, url_prefix='/')


if __name__ == "__main__":
        app.run()
