from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean, Enum, Date
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum


# Models Matkul Prasyarat
class MatkulPrasyarat(Base):
    __tablename__ = 'matkul_prasyarat'
    id = Column(Integer, primary_key = True, index = True)
    id_matkul = Column(Integer, ForeignKey('matkul.id', ondelete = "CASCADE", onupdate = "CASCADE"))
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    matkul_prasyarat = relationship("Matkul", back_populates = "matkul_prasyarats")
    matkul_prasyarat_details = relationship("MatkulPrasyaratDetail", back_populates = "matkul_prasyarat_detail")

# End Models Matkul Prasyarat
