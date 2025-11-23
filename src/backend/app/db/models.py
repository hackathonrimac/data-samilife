from sqlalchemy import Column, String, Integer, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from app.db.database import Base

class Institucion(Base):
    __tablename__ = "institucion"
    
    cod_inst = Column(String, primary_key=True, index=True)
    coord = Column(String)
    direccion = Column(String)
    nombre = Column(String)
    calificacion = Column(Float) # Agregado según tu corrección

class Aseguro(Base):
    __tablename__ = "aseguro"
    
    seguro = Column(String, primary_key=True)
    cod_inst = Column(String, ForeignKey("institucion.cod_inst"), primary_key=True)
    red = Column(String)
    costo = Column(Float)

class Medicina(Base):
    __tablename__ = "medicina"
    
    cod_med = Column(String, primary_key=True)
    nombre = Column(String)
    formato = Column(String)
    tipo = Column(String)

class MedEnInst(Base):
    __tablename__ = "med_en_inst"
    
    cod_inst = Column(String, ForeignKey("institucion.cod_inst"), primary_key=True)
    cod_med = Column(String, ForeignKey("medicina.cod_med"), primary_key=True)
    precio = Column(Float)
    stock = Column(Integer)

class Profesional(Base):
    __tablename__ = "profesional"
    
    cod_prof = Column(String, primary_key=True)
    profesion = Column(String, primary_key=True)
    nombre = Column(String)
    especialidad = Column(String)

class Servicio(Base):
    __tablename__ = "servicio"
    
    # FKs compuestas y PKs compuestas
    cod_inst = Column(String, ForeignKey("institucion.cod_inst"), primary_key=True)
    cod_prof = Column(String, primary_key=True) 
    profesion = Column(String, primary_key=True) # FK lógica hacia Profesional
    
    servicio_nombre = Column(String, primary_key=True, name="servicio") # 'servicio' es palabra reservada a veces, mejor usar alias interno
    telefono = Column(String)
    detalle = Column(JSON) # Aquí van los horarios