from pydantic import BaseModel
from typing import Optional
from fastapi import Query

class AgregarCarrito(BaseModel):
    id_cliente : int 
    id_producto : int
    nombre_producto : str
    proveedor : str
    cantidad_de_unidades : int
    precio_por_unidad: float
    tipo_producto : Optional[str] = Query("https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftumundoeconomia.com%2Fwp-content%2Fuploads%2F2020%2F07%2Fnecesidades-del-mercado6.png&f=1&nofb=1", max_length=200)
    url_imagen : str
    class Config:
        schema_extra = {
            "example": {
                "id_cliente": 1,
                "id_producto": 1,
                "nombre_producto": "Leche",
                "proveedor": "Zaragoza",
                "cantidad_de_unidades": 1,
                "precio_por_unidad":50.0,
                "tipo_producto":"Lacteos",
                "url_imagen":"http.imagen.1.png"
                }
            }

class SalidaCarrito(BaseModel):
    nombre_producto : str
    cantidad_de_unidades : int
    precio_por_unidad: float
    tipo_producto : str