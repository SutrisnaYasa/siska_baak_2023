from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean, Enum, Date
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

# Models Mahasiswa IRS
class MahasiswaIrs(Base):
    __tablename__ = 'mahasiswa_irs'
    id = Column(Integer, primary_key = True, index = True)
    id_mahasiswa = Column(Integer, ForeignKey('mahasiswa.id_mahasiswa', ondelete = "CASCADE", onupdate = "CASCADE"))
    id_matkul = Column(Integer, ForeignKey('matkul.id', ondelete = "CASCADE", onupdate = "CASCADE"))
    id_dosen_mengajar = Column(Integer, ForeignKey('dosen_mengajar.id', ondelete = "CASCADE", onupdate = "CASCADE"))
    tgl_setuju = Column(Date)
    id_grade = Column(Integer, ForeignKey('grade.id', ondelete = "CASCADE", onupdate = "CASCADE"))
    id_tahun_ajar = Column(Integer, ForeignKey('tahun_ajar.id', ondelete = "CASCADE", onupdate = "CASCADE"))
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    irs_mhs = relationship("Mahasiswa", back_populates = "irs_mhss")
    irs_matkul = relationship("Matkul", back_populates = "irs_matkuls")
    irs_grade = relationship("Grade", back_populates = "irs_grades")
    irs_tahun_ajar = relationship("TahunAjar", back_populates = "irs_tahun_ajars")
    mhs_nilai_irss = relationship("MahasiswaIrsNilai", back_populates = "mhs_nilai_irs")
    mhs_dosen_mengajars = relationship("DosenMengajar", back_populates = "mhs_dosen_mengajar")
# End Models Mahasiswa IRS
