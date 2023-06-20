from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean, Enum, Date
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

# Models Matkul
class Matkul(Base):
    __tablename__ = 'matkul'
    id = Column(Integer, primary_key = True, index = True)
    kode_matkul = Column(String(100))
    nama_matkul = Column(String(100))
    id_matkul_kelompok = Column(Integer, ForeignKey('matkul_kelompok.id', ondelete="CASCADE", onupdate="CASCADE"))
    status_aktif = Column(String(100))
    status_wajib = Column(String(100))
    id_prodi = Column(Integer, ForeignKey('prodi.id_prodi', ondelete="CASCADE", onupdate="CASCADE"))
    deskripsi = Column(String(100))
    semester_buka = Column(String(100))
    id_kurikulum = Column(Integer, ForeignKey('kurikulum.id', ondelete="CASCADE", onupdate="CASCADE"))
    simulasi = Column(Integer)
    praktik_lapangan = Column(Integer)
    pratikum = Column(Integer)
    tatap_muka = Column(Integer)
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    matkul_prodis = relationship("Prodi", back_populates = "matkul_prodi")
    matkul_kurikulums = relationship("Kurikulum", back_populates = "matkul_kurikulum")
    matkul_kelompoks = relationship("MatkulKelompok", back_populates = "matkul_kelompok")
    matkul_prasyarats = relationship("MatkulPrasyarat", back_populates = "matkul_prasyarat")
    mkl_prasyarat_details = relationship("MatkulPrasyaratDetail", back_populates = "mkl_prasyarat_detail")
    mengajar_matkuls = relationship("DosenMengajar", back_populates = "mengajar_matkul")
    mhs_trf_nilai_konversi_matkuls = relationship("MhsTrfNilaiKonversi", back_populates = "mhs_trf_nilai_konversi_matkul")
    irs_matkuls = relationship("MahasiswaIrs", back_populates = "irs_matkul")
# End Models Matkul
