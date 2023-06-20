from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean, Enum, Date
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

# Models Mahasiswa Ortu
class MahasiswaOrtu(Base):
    __tablename__ = 'mahasiswa_ortu'
    id_mhs_ortu = Column(Integer, primary_key = True, index = True)
    id_mahasiswa = Column(Integer, ForeignKey('mahasiswa.id_mahasiswa', ondelete="CASCADE", onupdate="CASCADE"))
    status_hubungan = Column(String(100))
    nik = Column(String(100))
    nama_ortu = Column(String(100))
    no_hp_ortu = Column(String(100))
    tgl_lahir_ortu = Column(Date)
    pendidikan = Column(String(100))
    pekerjaan = Column(String(100))
    penghasilan = Column(String(100))
    kebutuhan_khusus_ortu = Column(String(100))
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    mhsortu = relationship("Mahasiswa", back_populates = "mhsortus", cascade="all,delete")
# End Mahasiswa Ortu
