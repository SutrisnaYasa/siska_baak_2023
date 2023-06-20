from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean, Enum, Date
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

# Models Master Ruangan
class Ruangan(Base):
    __tablename__ = 'ruangan'
    id = Column(Integer, primary_key = True, index = True)
    nama_ruangan = Column(String(100))
    kapasitas = Column(Integer)
    gedung = Column(String(100))
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    mengajar_ruangans = relationship("DosenMengajar", back_populates = "mengajar_ruangan")
    dosen_jadwal_ujian_ruangans = relationship("DosenMengajarJadwalUjian", back_populates = "dosen_jadwal_ujian_ruangan")
# End Master Ruangan
