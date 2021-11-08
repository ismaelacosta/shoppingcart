from flask import Flask, jsonify, request
from sqlalchemy.orm import session
from api.utils.db import Session, engine, connection_db
from api.models.models import Carrito, Usuario, Ventas
import json
import requests


#migraciones base de datos


#Utilidad para seguridad por medio de tokens
from functools import wraps
import jwt
import datetime

"""Flask MIgrate
    sirve para añadir nuevas funciones a la base de datos como campos
"""
from flask_sqlalchemy import SQLAlchemy

#modulo para hash
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)

#no 

session = Session()

@app.route('/',methods=['GET'])
def hola():
    return jsonify({'message':"Prueba de funcionamiento....... HOLA!"})


#Metodo para añadir Es de Ejemplo para el proyecto
@app.route('/create_user',methods=['POST'])
def create_user():
    """print(request)
    print(dir(request))"""

    #Recibir los datos del POST y forzar a tenerlo en formato json 
    data = json.loads(request.data)
    #print("Aqui pone la info")
    print(data)
    print(type(data))

    #Validaciones
    if 'username' not in data:
        return jsonify({"respuesta":"Falta el id de la aplicacion"})
    if 'password' not in data:
        return jsonify({"respuesta":"Falta la descripcion de la aplicacion"})
    if len(data["username"])==0:
        return jsonify({"respuesta":"username no puede estar vacio"})
    if len(data["password"])==0:
        return jsonify({"respuesta":"password no puede estar vacio"})

    with engine.connect() as con:
        #Generar Hash a la contraseña
        hash_password = generate_password_hash(data["password"],method="sha256")
        nuevo_usuario = Usuario(username=data["username"],password=hash_password)
        session.add(nuevo_usuario)
        try:
            session.commit()
        except:
            return jsonify({"respuesta":"usuario ya creado en la base de datos"})
    return jsonify({"respuesta":"usuario creado correctamente"})

#Metodo de consulta de ventas de un usuario
@app.route('/obtener_venta',methods=['GET'])
def obtener_venta():
    data = json.loads(request.data)
    print(data)
    if 'username' not in data:
        return jsonify({"Respuesta":"username no enviado, validar datos!!"})
    
    with engine.connect() as con:
        obtener_usuario = f"select * from usuario where username= '{data['username']}'"
        respuesta = con.execute(obtener_usuario).one()
        print(respuesta)
        for i in respuesta:
            print(i)
        obtener_venta = f"select venta from ventas where username_id= '{respuesta[0]}'"
        respuesta_venta = con.execute(obtener_venta)
        print(respuesta_venta)
        respuesta_venta = [i[0] for i in respuesta_venta]
        print(respuesta_venta)
        return jsonify({"ventas_usuario":{"usuario":data['username'],"ventas":respuesta_venta}})


#Ejemplo para consultar datos de todo 
@app.route('/ventas', methods=['GET'])
def ventas():
    with engine.connect() as con:
        obtener_ventas2 = f"select * from ventas"
        respuesta_ventas2 = con.execute(obtener_ventas2)
        diccionario = list()

        for i in respuesta_ventas2:
            diccionario.append({"ID_Venta":i[0], "Valor venta": i[2]})
    return jsonify({"Ventas":diccionario})

#Ejemplo modificacion datos
@app.route('/ventas', methods=["PUT"])
def cambiar_venta():
    data = json.loads(request.data)
    if 'id' not in data:
        return jsonify({"Respuesta":"Id no enviado para su consulta"})
    if 'valor' not in data:
        return jsonify({"Respuesta":"venta no enviado para su consulta"})
    with engine.connect() as con:
        modificar_venta = f"update ventas set venta='{data['valor']}' where id= '{data['id']}'"
        respuesta2 = con.execute(modificar_venta)
        #session.commit()
    return jsonify({"Respuesta":"OK"})


   #Eliminar 
@app.route('/ventas',methods=['DELETE']) 
def eliminar_venta():
    data = json.loads(request.data)
    if 'id' not in data:
        return jsonify({"Respuesta":"Id no enviado para su consulta"})
    with engine.connect() as con:
        modificar_venta = f"delete from ventas where id= '{data['id']}'"
        respuesta2 = con.execute(modificar_venta)
    return jsonify({"Respuesta":"OK"})

if __name__ == "__main__":
        app.run()
