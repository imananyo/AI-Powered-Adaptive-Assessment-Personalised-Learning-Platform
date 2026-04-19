from sqlalchemy import Column, Integer, String, JSON
from app.db.database import Base


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, nullable=False)
    difficulty = Column(String, nullable=False)
    questions = Column(JSON, nullable=False)


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    evaluation = Column(JSON)