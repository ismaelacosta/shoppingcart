from pydantic import BaseModel
from typing import Optional

class AgregarCarrito(BaseModel):
    id_cliente : int 
    id_producto : int
    nombre_producto : str
    proveedor : str
    cantidad_de_unidades : int
    precio_por_unidad: float
    tipo_producto : str
    class Config:
        schema_extra = {
            "examplo": {
                "id_cliente": 1,
                "id_producto": 1,
                "nombre_producto": "Leche",
                "proveedor": "Zaragoza",
                "cantidad_de_unidades": 1,
                "precio_por_unidad":50.0,
                "tipo_producto":"Lacteos"
                }
            }

class SalidaCarrito(BaseModel):
    nombre_producto : str
    cantidad_de_unidades : int
    precio_por_unidad: float
    tipo_producto : str