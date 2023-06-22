from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean, Enum, Date
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from models.ruangan import Ruangan
from models.tahun_ajar import TahunAjar
from models.dosen_mengajar_kontrak import DosenMengajarKontrak

# Models Dosen Mengajar
class DosenMengajar(Base):
    __tablename__ = 'dosen_mengajar'
    id = Column(Integer, primary_key = True, index = True)
    id_dosen = Column(Integer, ForeignKey('dosen.id_dosen', ondelete = "CASCADE", onupdate = "CASCADE"))
    id_matkul = Column(Integer, ForeignKey('matkul.id', ondelete = "CASCADE", onupdate = "CASCADE" ))
    hari = Column(String(100))
    jam_mulai = Column(String(100))
    jam_akhir = Column(String(100))
    id_ruangan = Column(Integer, ForeignKey('ruangan.id', ondelete = "CASCADE", onupdate = "CASCADE" ))
    kelas = Column(String(100))
    id_tahun_ajar = Column(Integer, ForeignKey('tahun_ajar.id', ondelete = "CASCADE", onupdate = "CASCADE" ))
    jml_kursi = Column(String(100))
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    mengajar_dosen = relationship("Dosen", back_populates = "mengajar_dosens")
    mengajar_matkul = relationship("Matkul", back_populates = "mengajar_matkuls")
    mengajar_ruangan = relationship("Ruangan", back_populates = "mengajar_ruangans")
    mengajar_tahun_ajar = relationship("TahunAjar", back_populates = "mengajar_tahun_ajars")
    mengajar_dosen_kontraks = relationship("DosenMengajarKontrak", back_populates = "mengajar_dosen_kontrak")
    dosen_jadwal_ujians = relationship("DosenMengajarJadwalUjian", back_populates = "dosen_jadwal_ujian")
    mhs_dosen_mengajar = relationship("MahasiswaIrs", back_populates = "mhs_dosen_mengajars")
# End Models Dosen Mengajar
