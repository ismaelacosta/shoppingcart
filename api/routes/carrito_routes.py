from flask import Blueprint
from flask import Flask, jsonify, request
import json
import requests
from api.utils.db import engine


carrito_blueprint = Blueprint('carrito_blueprint', __name__)

@carrito_blueprint.route('/',methods=['GET'])
def hola():
    return jsonify({'mensaje':"Prueba de funcionamiento....... Hola"})

 #Metodo para añadir productos al carrito de las personas
@carrito_blueprint.route('/add_carrito',methods=['POST'])
def agregar_carrito():
    #Recibir los datos del POST y forzar a tenerlo en formato json 
    data = json.loads(request.data)
    #print("Aqui sirve para poner la informacion en consola")
    #print(data)
    #print(type(data))

    #Validaciones de los datos recibidos
    if 'id_cliente' not in data:
        return jsonify({"respuesta":"Falta el id del cliente"})
    if 'id_producto' not in data:
        return jsonify({"respuesta":"Falta el id del producto"})
    if 'nombre_producto' not in data:
        return jsonify({"respuesta":"Falta el nombre del producto"})
    if 'proveedor' not in data:
        return jsonify({"respuesta":"Falta el nombre del proveedor"})
    if 'nombre_producto' not in data:
        return jsonify({"respuesta":"Falta el nombre del producto"})
    if 'cantidad_de_unidades' not in data:
        return jsonify({"respuesta":"Falta el campo de cantidad de unidades"})
    if 'tipo_producto' not in data:
        return jsonify({"respuesta":"Falta el campo tipo de producto"})

    #Evalua si el contenido del json no es nulo    
    """if len(data["id_cliente"])==0:
        return jsonify({"respuesta":"username no puede estar vacio"})
    if len(data["id_producto"])==0:
        return jsonify({"respuesta":"password no puede estar vacio"})"""

    #Ejecutar instrucciones en nuestra base de datos
    with engine.connect() as con:
        insertar_carrito = f"insert into carrito (id_producto,id_cliente,nombre_producto,proveedor,cantidad_de_unidades,precio_por_unidad,tipo_producto,fecha_registro) values({data['id_producto']},{data['id_cliente']},'{data['nombre_producto']}','{data['proveedor']}',{data['cantidad_de_unidades']},{data['precio_por_unidad']},'{data['tipo_producto']}',NOW())"
        try:
            ejecutar = con.execute(insertar_carrito)
        except:
            return jsonify({"respuesta":"producto del usuario en el carrito ya creado en la base de datos"})
    return jsonify({"respuesta":"Producto agregado correctamente en el carrito"}) 

#Eliminar un producto de un cliente en especifico
@carrito_blueprint.route('/eliminar/<idcliente>/<idproducto>',methods=['DELETE']) 
def eliminar_carrito(idcliente,idproducto):
    #data = json.loads(request.data)
    """if 'id' not in data:
        return jsonify({"Respuesta":"Id no enviado para su consulta"})"""
    with engine.connect() as con:
        consulta_eliminar = f"delete from carrito where id_cliente= {idcliente} and id_producto={idproducto}"
        ejecutar_eliminacion = con.execute(consulta_eliminar)
    return jsonify({"Respuesta":"OK"}) 

#Metodo de consulta de carrito de un usuario en especifico
@carrito_blueprint.route('/obtener_carrito_cliente/<idcliente>',methods=['GET'])
def obtener_carrito_cliente(idcliente):
    #data = json.loads(request.data)
    #print(data)
    #if 'username' not in data:
    #    return jsonify({"Respuesta":"username no enviado, validar datos!!"})
    
    with engine.connect() as con:
        obtener_el_carrito_cliente = f"select * from carrito where id_cliente={idcliente}"
        respuesta_carrito = con.execute(obtener_el_carrito_cliente)
        diccionario = list()

        for i in respuesta_carrito:
            diccionario.append({"nombre_producto":i[3], "precio_por_unidad":i[6],"cantidad_de_unidades":i[5]})
    return jsonify({"Carrito":diccionario})

#Metodo para modificar aumentando la cantidad del producto de un cliente en especifico
@carrito_blueprint.route('/modificar_carrito_add/<idcliente>/<idproducto>', methods=["PUT"])
def cambiar_carrito_agregar(idcliente,idproducto):
    #data = json.loads(request.data)
    """if 'id' not in data:
        return jsonify({"Respuesta":"Id no enviado para su consulta"})
    if 'valor' not in data:
        return jsonify({"Respuesta":"venta no enviado para su consulta"})"""
    with engine.connect() as con:
        #consultar_cantidad = f"select cantidad_de_unidades from"
        modificar_venta = f"update carrito set cantidad_de_unidades=cantidad_de_unidades + 1 where id_cliente= {idcliente} and id_producto={idproducto}"
        respuesta2 = con.execute(modificar_venta)
        #session.commit()
    return jsonify({"Respuesta":"OK"})

#Metodo para modificar disminuyendo la cantidad del producto de un cliente en especifico
#En caso de que el producto llegue a cero este sera eliminado en su lugar
@carrito_blueprint.route('/modificar_carrito_borrar/<idcliente>/<idproducto>', methods=["PUT"])
def cambiar_carrito_borrar(idcliente,idproducto):
    #data = json.loads(request.data)
    """if 'id' not in data:
        return jsonify({"Respuesta":"Id no enviado para su consulta"})
    if 'valor' not in data:
        return jsonify({"Respuesta":"venta no enviado para su consulta"})"""
    with engine.connect() as con:
        consultar_cantidad = f"select cantidad_de_unidades from carrito where id_cliente= {idcliente} and id_producto={idproducto}"
        respuesta_cantidad = con.execute(consultar_cantidad)
        for i in respuesta_cantidad:
            cantidad_de_producto_consulta = i[0]
        if cantidad_de_producto_consulta == 1:
            consulta_eliminar = f"delete from carrito where id_cliente= {idcliente} and id_producto={idproducto}"
            ejecutar_eliminacion = con.execute(consulta_eliminar)
        else:
            modificar_venta = f"update carrito set cantidad_de_unidades=cantidad_de_unidades - 1  where id_cliente= {idcliente} and id_producto={idproducto}"
            respuesta2 = con.execute(modificar_venta) 
    return jsonify({"Respuesta":"OK"})