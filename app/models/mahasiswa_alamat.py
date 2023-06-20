from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean, Enum, Date
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

# Models Mahasiswa Alamat
class MahasiswaAlamat(Base):
    __tablename__ = 'mahasiswa_alamat'
    id_mhs_alamat = Column(Integer, primary_key = True, index = True)
    id_mahasiswa = Column(Integer, ForeignKey('mahasiswa.id_mahasiswa', ondelete="CASCADE", onupdate="CASCADE"))
    alamat_rmh = Column(String(100))
    provinsi = Column(String(100))
    kab_kota = Column(String(100))
    kecamatan = Column(String(100))
    kelurahan = Column(String(100))
    dusun = Column(String(100))
    rt = Column(String(100))
    rw = Column(String(100))
    kode_pos = Column(String(100))
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    mhsalamat = relationship("Mahasiswa", back_populates = "mhsalamats", cascade="all,delete")
# End Mahasiswa Alamat
