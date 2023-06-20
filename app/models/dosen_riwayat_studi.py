from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean, Enum, Date
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

# Models Dosen Riwayat Studi
class DosenRiwayatStudi(Base):
    __tablename__ = 'dosen_riwayatstudi'
    id = Column(Integer, primary_key = True, index = True)
    id_dosen = Column(Integer, ForeignKey('dosen.id_dosen', ondelete = "CASCADE", onupdate = "CASCADE"))
    jenjang_pendidikan = Column(String(100))
    nama_kampus = Column(String(100))
    fakultas = Column(String(100))
    prodi = Column(String(100))
    gelar = Column(String(100))
    tahun_masuk = Column(String(100))
    tahun_lulus = Column(String(100))
    sks_lulus = Column(Integer)
    ipk = Column(Float)
    judul_tugas_akhir = Column(String(100))
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    dosenriwayatstudis = relationship("Dosen", back_populates = "dosen_riwayatstudis")
# End Dosen Riwayat Studi Models
