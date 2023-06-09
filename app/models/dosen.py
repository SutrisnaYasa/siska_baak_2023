from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean, Enum, Date
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from models.dosen_alamat import DosenAlamat
from models.dosen_riwayat_studi import DosenRiwayatStudi
from models.dosen_jabfung import DosenJabfung
from models.matkul_kelompok import MatkulKelompok
from models.dosen_bimbingan_pa import DosenBimbinganPa

# Models Dosen
class Dosen(Base):
    __tablename__ = 'dosen'
    id_dosen = Column(Integer, primary_key = True, index = True)
    kode_dosen = Column(String(100))
    nidk = Column(String(100))
    nidn = Column(String(100))
    npwp = Column(String(100))
    nama = Column(String(100))
    jenis_kelamin = Column(String(100))
    no_hp = Column(String(100))
    email = Column(String(100))
    id_prodi = Column(Integer, ForeignKey('prodi.id_prodi', ondelete="CASCADE", onupdate="CASCADE"))
    tempat_lahir = Column(String(100))
    tgl_lahir = Column(Date)
    agama = Column(String(100))
    nama_ibu_kandung = Column(String(100))
    status_kedosenan = Column(String(100))
    status_aktif = Column(
        Integer,
        nullable = False,
        default = 1,
        comment = 'Status Dosen: 0 - Nonaktif, 1 - Aktif, 2 - Cuti, 3 - Resign'
    )
    status_perkawinan = Column(String(100))
    hubungan_pasangan = Column(String(100))
    nik_pasangan = Column(String(100))
    pekerjaan_pasangan = Column(String(100))
    no_sk_pengangkatan_dosen = Column(String(100))
    mulai_sk_pengangkatan_dosen = Column(Date)
    tgl_sk_nidn = Column(Date)
    sumber_gaji = Column(String(100))
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    dosens = relationship("Prodi", back_populates = "dosen_prodi")
    dosen_alamats = relationship("DosenAlamat", back_populates = "dosenalamats")
    dosen_riwayatstudis = relationship("DosenRiwayatStudi", back_populates = "dosenriwayatstudis")
    dosen_jabfung = relationship("DosenJabfung", back_populates = "dosenjabfungs")
    matkul_klp_dosens = relationship("MatkulKelompok", back_populates = "matkul_klp_dosen")
    dosen_bimbingan_pa_dosens_1 = relationship("DosenBimbinganPa", foreign_keys=[DosenBimbinganPa.dosen_pa_1], back_populates="dosen_bimbingan_pa_dosen_1")
    dosen_bimbingan_pa_dosens_2 = relationship("DosenBimbinganPa", foreign_keys=[DosenBimbinganPa.dosen_pa_2], back_populates="dosen_bimbingan_pa_dosen_2")
    mengajar_dosens = relationship("DosenMengajar", back_populates="mengajar_dosen")
    mengajar_dosens = relationship("DosenMengajar", back_populates = "mengajar_dosen")
# End Dosen Models
