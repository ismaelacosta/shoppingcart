from pydantic import BaseModel
from typing import Optional

class Carrito(BaseModel):
    id_cliente : int 
    id_producto : int
    nombre_producto : str
    proveedor : str
    cantidad_de_unidades : int
    precio_por_unidad: int
    tipo_producto : str

