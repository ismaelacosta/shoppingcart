#Se guardan las tablas 
from sqlalchemy import Column,String,Integer
from sqlalchemy.sql.sqltypes import TIMESTAMP, Float, Numeric
from api.utils.db import Base, engine
from api.models import models
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship

class Carrito(Base):
    __tablename__ = 'carrito'
    id = Column(Integer, autoincrement=True, primary_key=True)
    id_producto = Column(Integer, nullable=False)
    id_cliente = Column(Integer, nullable=False)
    nombre_producto = Column(String(40))
    proveedor = Column(String(40))
    cantidad_de_unidades = Column(Integer)
    precio_por_unidad = Column(Numeric)
    tipo_producto = Column(String(40))
    url_imagen = Column(String(200))
    fecha_registro = Column(TIMESTAMP)
    
models.Base.metadata.create_all(engine)#Crea la table en base de datos 