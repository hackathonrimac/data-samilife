"""SQLAlchemy ORM models for healthcare database."""

from sqlalchemy import Column, String, Float, Integer, Date, ForeignKey, ForeignKeyConstraint
from geoalchemy2 import Geography
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Institucion(Base):
    """Healthcare institution/establishment model."""
    
    __tablename__ = "institucion"
    
    cod_unico = Column(String, primary_key=True)
    direccion = Column(String)
    institucion = Column(String)  # público/privado
    establecimiento = Column(String)
    clasificacion = Column(String)
    correo = Column(String)
    files = Column(String)
    longitud = Column(String)  # DB stores text; keep as string to avoid type mismatch
    latitud = Column(String)   # DB stores text; keep as string to avoid type mismatch
    pagina = Column(String)
    f_longitud = Column(Float)  # Converted float value
    f_latitud = Column(Float)   # Converted float value
    location = Column(Geography(geometry_type='POINT', srid=4326))  # PostGIS point
    
    # Relationships
    servicios = relationship("Servicio", back_populates="institucion_rel")
    medicamentos = relationship("MedicInst", back_populates="institucion_rel")
    seguros = relationship("Asegurado", back_populates="institucion_rel")


class Profesional(Base):
    """Medical professional model."""
    
    __tablename__ = "profesional"
    
    cmp = Column(String, primary_key=True)
    profesion = Column(String, primary_key=True)
    nombre_profesional = Column(String)
    especialidad = Column(String)
    
    # Relationships
    servicios = relationship("Servicio", back_populates="profesional_rel")


class Servicio(Base):
    """Healthcare service model."""
    
    __tablename__ = "servicio"
    
    cod_unico = Column(String, ForeignKey("institucion.cod_unico"), primary_key=True)
    cmp = Column(String, primary_key=True)
    profesion = Column(String, primary_key=True)
    servicio = Column(String, primary_key=True)
    detalle = Column(String)  # JSON string with schedule
    telefono = Column(String)
    actividad = Column(String)
    
    # Composite foreign key to Profesional
    __table_args__ = (
        ForeignKeyConstraint(
            ['cmp', 'profesion'],
            ['profesional.cmp', 'profesional.profesion']
        ),
    )
    
    # Relationships
    institucion_rel = relationship("Institucion", back_populates="servicios")
    profesional_rel = relationship("Profesional", back_populates="servicios")


class Medicamentos(Base):
    """Medication/pharmaceutical product model."""
    
    __tablename__ = "medicamentos"
    
    codigo_med = Column(String, primary_key=True)
    nombre_med = Column(String)
    formaf = Column(String)  # pharmaceutical form
    tipomed = Column(String)
    
    # Relationships
    instituciones = relationship("MedicInst", back_populates="medicamento_rel")


class MedicInst(Base):
    """Medication-Institution relationship model (stock and pricing)."""
    
    __tablename__ = "medic_inst"
    
    cod_unico = Column(String, ForeignKey("institucion.cod_unico"), primary_key=True)
    codigo_med = Column(String, ForeignKey("medicamentos.codigo_med"), primary_key=True)
    stock_tot = Column(Integer)
    indicador = Column(String)
    precio = Column(Float)
    fecha_venc = Column(Date)
    
    # Relationships
    institucion_rel = relationship("Institucion", back_populates="medicamentos")
    medicamento_rel = relationship("Medicamentos", back_populates="instituciones")


class Asegurado(Base):
    """Insurance coverage model."""
    
    __tablename__ = "asegurado"
    
    cod_unico = Column(String, ForeignKey("institucion.cod_unico"), primary_key=True)
    seguro = Column(String, primary_key=True)
    red = Column(String)
    costo_consulta = Column(String)  # Stored as text in DB
    
    # Relationships
    institucion_rel = relationship("Institucion", back_populates="seguros")
