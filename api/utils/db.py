from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base #Permite realizar el mapeo a partir del modelo
from sqlalchemy.orm import sessionmaker


POSTGRES = {
    'user': 'lpvialnlgfvxbe',
    'pw': '30b442a4ba6d14770d995b09d8ed8bbbbafe9162b3af47dec6ea103c3d3f78e7',
    'db': 'derdfli8bkt30d',
    'host': 'ec2-3-221-100-217.compute-1.amazonaws.com',
    'port': '5432',
}

connection_db='postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

engine = create_engine(connection_db)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Guarda las transacciones a la base de datos

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()