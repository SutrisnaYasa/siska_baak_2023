from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean, Enum, Date
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

# Models Kurikulum
class Kurikulum(Base):
    __tablename__ = 'kurikulum'
    id = Column(Integer, primary_key = True, index = True)
    nama = Column(String(100))
    tahun = Column(String(100))
    tgl_start = Column(Date)
    sks_lulus = Column(Integer)
    sks_wajib = Column(Integer)
    sks_pilihan = Column(Integer)
    status_aktif = Column(String(100))
    id_prodi = Column(Integer, ForeignKey('prodi.id_prodi', ondelete="CASCADE", onupdate="CASCADE"))
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    kurikulums = relationship("Prodi", back_populates = "kurikulum_prodi")
    matkul_kurikulum = relationship("Matkul", back_populates = "matkul_kurikulums")
# End Models Kurikulum
