from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean, Enum, Date
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

# Models Mahasiswa Transfer
class MahasiswaTransfer(Base):
    __tablename__ = 'mahasiswa_transfer'
    id_mhs_transfer =  Column(Integer, primary_key = True, index = True)
    id_mahasiswa = Column(Integer, ForeignKey('mahasiswa.id_mahasiswa', ondelete="CASCADE", onupdate="CASCADE"))
    kampus_asal = Column(String(100))
    nim_asal = Column(String(100))
    ipk_lama = Column(Float)
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    mhstransfer = relationship("Mahasiswa", back_populates = "mhstransfers", cascade="all,delete")
    mhs_trf_nilai_konversis = relationship("MhsTrfNilaiKonversi", back_populates = "mhs_trf_nilai_konversi")
# End Mahasiswa Transfer
