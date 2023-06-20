from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean, Enum, Date
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

# Models Master Prodi
class Prodi(Base):
    __tablename__ = 'prodi'
    id_prodi = Column(Integer, primary_key = True, index = True)
    kode_prodi = Column(String(100))
    nama_prodi = Column(String(100))
    id_fakultas = Column(Integer, ForeignKey('fakultas.id_fakultas', ondelete="CASCADE", onupdate="CASCADE"))
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    prodis = relationship("Fakultas", back_populates = "fakultass")
    dosen_prodi = relationship("Dosen", back_populates = "dosens")
    mhs_prodi = relationship("Mahasiswa", back_populates = "mhss")
    kurikulum_prodi = relationship("Kurikulum", back_populates = "kurikulums")
    matkul_prodi = relationship("Matkul", back_populates = "matkul_prodis")
# End Master Prodi
