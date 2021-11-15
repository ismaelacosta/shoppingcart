from fastapi import APIRouter
import json
import requests

from api.models.carrito import Carrito
from api.utils.db import engine

router = APIRouter()

@router.get("/")
def hola():
    return {'mensaje':"Prueba de funcionamiento....... Hola"}

 #Metodo para añadir productos al carrito de las personas
@router.post("/add_carrito")
def agregar_carrito(data : Carrito):
    #Recibir los datos del POST y forzar a tenerlo en formato json 
    #print("Aqui sirve para poner la informacion en consola")
    #print(data)
    #print(type(data))
    
    #Ejecutar instrucciones en nuestra base de datos
    with engine.connect() as con:
        insertar_carrito = f"insert into carrito (id_producto,id_cliente,nombre_producto,proveedor,cantidad_de_unidades,precio_por_unidad,tipo_producto,fecha_registro) values({data.id_producto},{data.id_cliente},'{data.nombre_producto}','{data.proveedor}',{data.cantidad_de_unidades},{data.precio_por_unidad},'{data.tipo_producto}',NOW())"
        try:
            ejecutar = con.execute(insertar_carrito)
        except:
            return {"respuesta":"producto del usuario en el carrito ya creado en la base de datos"}
    return {"respuesta":"Producto agregado correctamente en el carrito"}

#Eliminar un producto de un cliente en especifico
@router.delete("/eliminar/{idcliente}/{idproducto}") 
def eliminar_carrito(idcliente,idproducto):
    with engine.connect() as con:
        consulta_eliminar = f"delete from carrito where id_cliente= {idcliente} and id_producto={idproducto}"
        ejecutar_eliminacion = con.execute(consulta_eliminar)
    return {"Respuesta":"OK"}

#Metodo de consulta de carrito de un usuario en especifico
@router.get("/obtener_carrito_cliente/{idcliente}")
def obtener_carrito_cliente(idcliente):
    with engine.connect() as con:
        obtener_el_carrito_cliente = f"select * from carrito where id_cliente={idcliente}"
        respuesta_carrito = con.execute(obtener_el_carrito_cliente)
        diccionario = list()

        for i in respuesta_carrito:
            diccionario.append({"nombre_producto":i[3], "precio_por_unidad":i[6],"cantidad_de_unidades":i[5]})
    return {"Carrito":diccionario}

#Metodo para modificar aumentando la cantidad del producto de un cliente en especifico
@router.put("/modificar_carrito_add/{idcliente}/{idproducto}")
def cambiar_carrito_agregar(idcliente,idproducto):
   
    with engine.connect() as con:
        #consultar_cantidad = f"select cantidad_de_unidades from"
        modificar_venta = f"update carrito set cantidad_de_unidades=cantidad_de_unidades + 1 where id_cliente= {idcliente} and id_producto={idproducto}"
        respuesta2 = con.execute(modificar_venta)
        #session.commit()
    return {"Respuesta":"OK"}

#Metodo para modificar disminuyendo la cantidad del producto de un cliente en especifico
#En caso de que el producto llegue a cero este sera eliminado en su lugar
@router.put("/modificar_carrito_borrar/{idcliente}/{idproducto}")
def cambiar_carrito_borrar(idcliente,idproducto):
    #data = json.loads(request.data)
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
    return {"Respuesta":"OK"}
