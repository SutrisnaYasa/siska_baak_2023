from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean, Enum, Date
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

# Models Mahasiswa IRS Nilai
class MahasiswaIrsNilai(Base):
    __tablename__ = 'mahasiswa_irs_nilai'
    id = Column(Integer, primary_key = True, index = True)
    id_mahasiswa_irs = Column(Integer, ForeignKey('mahasiswa_irs.id', ondelete = "CASCADE", onupdate = "CASCADE"))
    keaktifan = Column(Float)
    tugas = Column(Float)
    uts = Column(Float)
    uas = Column(Float)
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    mhs_nilai_irs = relationship("MahasiswaIrs", back_populates = "mhs_nilai_irss")
# End Models Mahasiswa IRS Nilai
