from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean, Enum, Date
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from models.mahasiswa_irs import MahasiswaIrs

# Models Master Tahun Ajar
class TahunAjar(Base):
    __tablename__ = 'tahun_ajar'
    id = Column(Integer, primary_key = True, index = True)
    nama_tahun_ajar = Column(String(100))
    semester = Column(String(100))
    tanggal_mulai = Column(Date)
    tanggal_akhir = Column(Date)
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    mengajar_tahun_ajars = relationship("DosenMengajar", back_populates = "mengajar_tahun_ajar")
    irs_tahun_ajars = relationship("MahasiswaIrs", back_populates = "irs_tahun_ajar")
# End Master Tahun Ajar
