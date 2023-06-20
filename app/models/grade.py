from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Boolean, Enum, Date
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

# Models Grade
class Grade(Base):
    __tablename__ = 'grade'
    id = Column(Integer, primary_key = True, index = True)
    nilai_huruf = Column(String(100))
    bobot_awal = Column(Integer)
    bobot_akhir = Column(Integer)
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    deleted_at = Column(DateTime(timezone = True), default = None, nullable = True)
    irs_grades = relationship("MahasiswaIrs", back_populates = "irs_grade")
# End Models Grade
