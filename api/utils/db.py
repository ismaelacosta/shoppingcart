from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base #Permite realizar el mapeo a partir del modelo
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.selectable import Select #todo se hace por sesiones, tenemos que guardar las transacciones para guardar en la base de datos

POSTGRES = {
    'user': 'lpvialnlgfvxbe',
    'pw': '30b442a4ba6d14770d995b09d8ed8bbbbafe9162b3af47dec6ea103c3d3f78e7',
    'db': 'derdfli8bkt30d',
    'host': 'ec2-3-221-100-217.compute-1.amazonaws.com',
    'port': '5432',
}

connection_db='postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

Base = declarative_base()


engine = create_engine(connection_db)

Session = sessionmaker(bind=engine) # Guarda las transacciones a la base de datos
