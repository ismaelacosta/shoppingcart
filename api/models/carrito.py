from pydantic import BaseModel
from typing import Optional

class Carrito(BaseModel):
    id_carrito : Optional[int] = None
    id_cliente : int 
    id_producto : int
    nombre_producto : str
    proveedor : str
    cantidad_de_unidades : int
    tipo_producto : str
     
