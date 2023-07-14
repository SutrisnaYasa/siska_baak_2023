from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean, Enum, Date
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from sqlalchemy.dialects.mysql import TINYINT

# Models Dosen Bimbingan PA
class DosenBimbinganPa(Base):
    __tablename__ = 'dosen_bimbingan_pa'
    id = Column(Integer, primary_key = True, index = True)
    dosen_pa_1 = Column(Integer, ForeignKey('dosen.id_dosen', ondelete = "CASCADE", onupdate = "CASCADE"))
    dosen_pa_2 = Column(Integer, ForeignKey('dosen.id_dosen', ondelete = "CASCADE", onupdate = "CASCADE"))
    id_mahasiswa = Column(Integer, ForeignKey('mahasiswa.id_mahasiswa', ondelete = "CASCADE", onupdate = "CASCADE"))
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    dosen_bimbingan_pa_dosen_1 = relationship("Dosen", foreign_keys=[dosen_pa_1], back_populates="dosen_bimbingan_pa_dosens_1")
    dosen_bimbingan_pa_dosen_2 = relationship("Dosen", foreign_keys=[dosen_pa_2], back_populates="dosen_bimbingan_pa_dosens_2")
    dosen_bimbingan_pa_mhs = relationship("Mahasiswa", back_populates = "dosen_bimbingan_pa_mhss")
# End Models Dosen Bimbingan PA
