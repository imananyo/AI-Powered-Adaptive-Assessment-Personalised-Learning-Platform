from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import enum


class UserRole(str, enum.Enum):
    student = "student"
    teacher = "teacher"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.student, nullable=False)
    full_name = Column(String(100), nullable=True)
    is_active = Column(Integer, default=1)  # 1 = active, 0 = inactive

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    submissions = relationship("Submission", back_populates="student")

    def __repr__(self):
        return f"<User {self.email} - {self.role}>"


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String(200), nullable=False, index=True)
    difficulty = Column(String(20), nullable=False)
    questions = Column(JSON, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Assessment {self.topic} - {self.difficulty}>"


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=True)
    
    answer = Column(Text, nullable=False)
    evaluation = Column(JSON, nullable=True)
    
    score = Column(Integer)           # Overall score (0-100)
    depth_score = Column(Integer)     # Depth of understanding (0-100)
    
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    student = relationship("User", back_populates="submissions")

    def __repr__(self):
        return f"<Submission {self.id} - Student {self.student_id}>"