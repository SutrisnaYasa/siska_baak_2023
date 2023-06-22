from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean, Enum, Date
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from models.prodi import Prodi

# Models Master Fakultas
class Fakultas(Base):
    __tablename__ = 'fakultas'
    id_fakultas = Column(Integer, primary_key = True, index = True)
    kode_fakultas = Column(String(100))
    nama_fakultas = Column(String(100))
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    fakultass = relationship("Prodi", back_populates = "prodis", cascade="all,delete")
# End Master Fakultas
