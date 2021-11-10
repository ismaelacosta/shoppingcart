from flask import Flask, jsonify, request
from sqlalchemy.orm import session
#Localizar las direcciones en otras rutas
from flask import Blueprint

from api.utils.db import Session, engine, connection_db
from api.models.models import Carrito, Usuario, Ventas
import json
import requests


#migraciones base de datos


#Utilidad para seguridad por medio de tokens
from functools import wraps
import jwt
import datetime

#MOdulo para importar rutas de otro archivo
from api.routes.carrito import carrito_routes

"""Flask MIgrate
    sirve para añadir nuevas funciones a la base de datos como campos
"""
from flask_sqlalchemy import SQLAlchemy

#modulo para hash
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)

#no 

session = Session()

app.register_blueprint(carrito_routes, url_prefix='/')




if __name__ == "__main__":
        app.run()
