from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean, Enum, Date
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

# Models Matkul Prasyarat Detail
class MatkulPrasyaratDetail(Base):
    __tablename__ = 'matkul_prasyarat_detail'
    id = Column(Integer, primary_key = True, index = True)
    id_matkul_prasyarat = Column(Integer, ForeignKey('matkul_prasyarat.id', ondelete = "CASCADE", onupdate = "CASCADE"))
    id_syarat = Column(Integer, ForeignKey('matkul.id', ondelete = "CASCADE", onupdate = "CASCADE"))
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    mkl_prasyarat_detail = relationship("Matkul", back_populates = "mkl_prasyarat_details")
    relasi_matkul_prasyarat = relationship("MatkulPrasyarat", back_populates = "relasi_matkul_prasyarats")
   
# End Models Matkul Prasyarat Detail
