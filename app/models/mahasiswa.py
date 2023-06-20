from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean, Enum, Date
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

# Models Mahasiswa
class Mahasiswa(Base):
    __tablename__ = 'mahasiswa'
    id_mahasiswa = Column(Integer, primary_key = True, index = True)
    nim = Column(String(100))
    nik = Column(String(100))
    nisn = Column(String(100))
    nama = Column(String(100))
    tempat_lahir = Column(String(100))
    tgl_lahir = Column(Date)
    jenis_kelamin = Column(String(100))
    agama = Column(String(100))
    kewarganegaraan = Column(String(100))
    sekolah_asal = Column(String(100))
    id_prodi = Column(Integer, ForeignKey('prodi.id_prodi', ondelete="CASCADE", onupdate="CASCADE"))
    status_awal = Column(String(100))
    status_aktif = Column(String(100))
    angkatan = Column(String(100))
    kelas = Column(String(100))
    no_hp = Column(String(100))
    no_tlp = Column(String(100))
    email = Column(String(100))
    jenis_tinggal = Column(String(100))
    npwp = Column(String(100))
    alat_transportasi = Column(String(100))
    nomor_kps = Column(String(100))
    penerima_kps = Column(String(100))
    kebutuhan_khusus = Column(String(100))
    bidang_minat = Column(String(100))
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    mhss = relationship("Prodi", back_populates = "mhs_prodi")
    mhsalamats = relationship("MahasiswaAlamat", back_populates = "mhsalamat", cascade="all,delete")
    mhsortus = relationship("MahasiswaOrtu", back_populates = "mhsortu", cascade="all,delete")
    mhstransfers = relationship("MahasiswaTransfer", back_populates = "mhstransfer", cascade="all,delete")
    dosen_bimbingan_pa_mhss = relationship("DosenBimbinganPa", back_populates = "dosen_bimbingan_pa_mhs")
    irs_mhss = relationship("MahasiswaIrs", back_populates = "irs_mhs")
# End Mahasiswa
