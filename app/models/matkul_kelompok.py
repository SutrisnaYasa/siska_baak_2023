from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean, Enum, Date
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from models.matkul import Matkul

# Models Matkul Kelompok
class MatkulKelompok(Base):
    __tablename__ = 'matkul_kelompok'
    id = Column(Integer, primary_key = True, index = True)
    nama_kelompok_matkul = Column(String(100))
    id_dosen = Column(Integer, ForeignKey('dosen.id_dosen', ondelete="CASCADE", onupdate="CASCADE"))
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    matkul_kelompok = relationship("Matkul", back_populates = "matkul_kelompoks")
    matkul_klp_dosen = relationship("Dosen", back_populates = "matkul_klp_dosens")
# End Models Matkul Kelompok
