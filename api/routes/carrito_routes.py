from fastapi import APIRouter, Depends
import json
from typing import List 
from pydantic.errors import NotNoneError
from pydantic.typing import NONE_TYPES
import requests
from sqlalchemy.orm import Session, session
from sqlalchemy.sql.elements import Null

from api.models.carrito import AgregarCarrito, SalidaCarrito

from api.utils.db import engine, get_db

#MOdelos para la base de datos
from api.models.models import Carrito as modeloCarrrito

router = APIRouter()

@router.get("/")
def hola():
    return {'mensaje':"Prueba de funcionamiento....... Hola"}

 #Metodo para añadir productos al carrito de los clientes
@router.post("/agregar_carrito")
def agregar_carrito(data : AgregarCarrito):
    #Ejecutar instrucciones en nuestra base de datos
    with engine.connect() as con:
        verificar_entrada_carrito = f"select id_cliente from carrito where id_cliente={data.id_cliente} and id_producto ={data.id_producto}"
        insertar_carrito = f"insert into carrito (id_producto,id_cliente,nombre_producto,proveedor,cantidad_de_unidades,precio_por_unidad,tipo_producto,url_imagen,fecha_registro) values({data.id_producto},{data.id_cliente},'{data.nombre_producto}','{data.proveedor}',{data.cantidad_de_unidades},{data.precio_por_unidad},'{data.tipo_producto}','{data.url_imagen}',NOW())"
        validacion = None
        try:
            # Valida si el producto ya fue agregado antes en el carrito
            ejecutar_verificacion = con.execute(verificar_entrada_carrito)
            for i in ejecutar_verificacion:
                validacion = i[0]
            if validacion != None:
                return{"respuesta" : "El cliente ya tiene agregado el producto en el carrito" }
            else:
                #Ejecuta la instruccion para agregarlo en el carrito si no lo estaba previamente
                ejecutar = con.execute(insertar_carrito)
        except:
            return {"respuesta":"Error interno"}
    return {"respuesta":"Producto agregado correctamente en el carrito"}

#Eliminar un producto de un cliente en especifico
@router.delete("/eliminar/{idcliente}/{idproducto}") 
def eliminar_producto_carrito(idcliente: int ,idproducto : int):
    with engine.connect() as con:
        consulta_eliminar = f"delete from carrito where id_cliente= {idcliente} and id_producto={idproducto}"
        ejecutar_eliminacion = con.execute(consulta_eliminar)
    return {"Respuesta":"OK"}

#Eliminar todo el carrito de un cliente
@router.delete("/eliminar/{idcliente}") 
def eliminar_carrito_completo(idcliente : int , db : Session = Depends(get_db)):
    with engine.connect() as con:
        #consulta_eliminar = f"delete from carrito where id_cliente= {idcliente} and id_producto={idproducto}"
        try:
            orm = db.query(modeloCarrrito).filter(modeloCarrrito.id_cliente == idcliente).delete()
            db.commit()

        except:
            return {"Respuesta": "Error al eliminar el carrito del cliente"}
        #ejecutar_eliminacion = con.execute(consulta_eliminar)
    return {"Respuesta":"OK"}

#Metodo de consulta de carrito de un usuario en especifico
@router.get("/obtener_carrito_cliente/{idcliente}")
def obtener_carrito_cliente(idcliente: int, db: Session = Depends(get_db)):
    orm = db.query(modeloCarrrito).filter(modeloCarrrito.id_cliente == idcliente).all()
    diccionario = list()
    for i in orm:
        diccionario.append({"id_producto":i.id_producto,"nombre_producto":i.nombre_producto,"proveedor":i.proveedor, "precio_por_unidad":i.precio_por_unidad,"cantidad_de_unidades":i.cantidad_de_unidades,"url_imagen":i.url_imagen})
    
    return {"Carrito":diccionario}


#Metodo la fecha en que fueron registrados los productos en el carrito de todos
@router.get("/obtener_registro_carrito_clientes")
def obtener_registro_carritos_clientes(db: Session = Depends(get_db)):
    orm = db.query(modeloCarrrito).all()
    diccionario = list()
    for i in orm:
        diccionario.append({"id_cliente":i.id_cliente,"id_producto":i.id_producto,"fecha_registro":i.fecha_registro})

    return diccionario

#Metodo para modificar aumentando la cantidad del producto de un cliente en especifico
@router.put("/modificar_carrito_add/{idcliente}/{idproducto}")
def cambiar_carrito_agregar(idcliente : int ,idproducto : int):
    with engine.connect() as con:
        #consultar_cantidad = f"select cantidad_de_unidades from"
        modificar_venta = f"update carrito set cantidad_de_unidades=cantidad_de_unidades + 1 where id_cliente= {idcliente} and id_producto={idproducto}"
        respuesta2 = con.execute(modificar_venta)
        #session.commit()
    return {"Respuesta":"OK"}

#Metodo para modificar disminuyendo la cantidad del producto de un cliente en especifico
#En caso de que el producto llegue a cero este sera eliminado en su lugar
@router.put("/modificar_carrito_borrar/{idcliente}/{idproducto}")
def cambiar_carrito_borrar(idcliente : int, idproducto: int):
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
