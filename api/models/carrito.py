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
    #Definir los tipos de datos necesarios
    class Config:
        schema_extra = {
            "Ejemplo": {
                "id_cliente": 1,
                "id_producto": 1,
                "nombre_producto": "Leche",
                "proveedor": "Zaragoza",
                "cantidad_de_unidades": 1,
                "precio_por_unidad":50.0,
                "tipo_producto":"Lacteos"
                }
            }

