from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean, Enum, Date
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

# Models Mahasiswa Transfer Nilai Konversi
class MhsTrfNilaiKonversi(Base):
    __tablename__ = 'mahasiswa_transfer_nilai_konversi'
    id = Column(Integer, primary_key = True, index = True)
    id_mahasiswa_transfer = Column(Integer, ForeignKey('mahasiswa_transfer.id_mhs_transfer', ondelete = "CASCADE", onupdate = "CASCADE"))
    id_matkul_asal = Column(String(100))
    nama_matkul_asal = Column(String(100))
    sks_matkul_asal = Column(Integer)
    nilai_huruf_matkul_asal = Column(String(100))
    id_matkul = Column(Integer, ForeignKey('matkul.id', ondelete = "CASCADE", onupdate = "CASCADE"))
    nilai_akhir = Column(Float)
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    mhs_trf_nilai_konversi = relationship("MahasiswaTransfer", back_populates = "mhs_trf_nilai_konversis")
    mhs_trf_nilai_konversi_matkul = relationship("Matkul", back_populates = "mhs_trf_nilai_konversi_matkuls")
# End Models Mahasiswa Transfer Nilai Konversi
