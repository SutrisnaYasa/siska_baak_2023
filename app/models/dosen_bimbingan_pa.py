from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean, Enum, Date
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

# Models Dosen Bimbingan PA
class DosenBimbinganPa(Base):
    __tablename__ = 'dosen_bimbingan_pa'
    id = Column(Integer, primary_key = True, index = True)
    id_dosen = Column(Integer, ForeignKey('dosen.id_dosen', ondelete = "CASCADE", onupdate = "CASCADE"))
    id_mahasiswa = Column(Integer, ForeignKey('mahasiswa.id_mahasiswa', ondelete = "CASCADE", onupdate = "CASCADE"))
    status = Column(String(100))
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    dosen_bimbingan_pa_dosen = relationship("Dosen", back_populates = "dosen_bimbingan_pa_dosens")
    dosen_bimbingan_pa_mhs = relationship("Mahasiswa", back_populates = "dosen_bimbingan_pa_mhss")
# End Models Dosen Bimbingan PA
