from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean, Enum, Date
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

# Models Dosen Mengajar Jadwal Ujian
class DosenMengajarJadwalUjian(Base):
    __tablename__ = 'dosen_mengajar_jadwal_ujian'
    id = Column(Integer, primary_key = True, index = True)
    id_dosen_mengajar = Column(Integer, ForeignKey('dosen_mengajar.id', ondelete = "CASCADE", onupdate = "CASCADE"))
    jenis_ujian = Column(String(100))
    hari = Column(String(100))
    tgl = Column(Date)
    jam_mulai = Column(String(100))
    jam_akhir = Column(String(100))
    pengawas = Column(String(100))
    id_ruangan = Column(Integer, ForeignKey('ruangan.id', ondelete = "CASCADE", onupdate = "CASCADE"))
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    dosen_jadwal_ujian = relationship("DosenMengajar", back_populates = "dosen_jadwal_ujians")
    dosen_jadwal_ujian_ruangan = relationship("Ruangan", back_populates = "dosen_jadwal_ujian_ruangans")
# End Models Dosen Mengajar Jadwal Ujian
