#Se guardan las tablas 
from sqlalchemy import Column,String,Integer
from sqlalchemy.sql.sqltypes import TIMESTAMP
from api.utils.db import Base, engine
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
    precio_por_unidad = Column(Integer)
    tipo_producto = Column(String(40))
    fecha_registro = Column(TIMESTAMP)

class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(70), unique=True)
    password = Column(String(200))
    ventas = relationship("Ventas",backref="usuario")

    def __init__(self, username, password,ventas):
        self.username = username
        self.password = password
        self.ventas = ventas

    def __repr__(self):
        return '%s/%s/%s' % (self.id, self.username, self.password)


class Ventas(Base):
    __tablename__ ="ventas"
    id = Column(Integer, autoincrement=True, primary_key=True)
    username_id= Column(Integer,ForeignKey("usuario.id"))
    venta = Column(Integer)

    def __init__(self, username_id, venta):
        self.username_id = username_id
        self.venta = venta

    def __repr__(self):
        return '%s/%s/%s' % (self.id, self.username_id, self.venta)
    
Base.metadata.create_all(engine)