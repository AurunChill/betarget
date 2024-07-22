import enum
from datetime import date

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, relationship, mapped_column

from base import Base


# Enums
class Gender(enum.Enum):
    male = 'male'
    female = 'female'
    other = 'other'


class InterestInJob(enum.Enum):
    """Candidate's job interest status"""
    looking_for_job = 'looking for job'
    not_looking_for_a_job = 'not looking for a job'
    considers_proposals = 'considers proposals'
    offered_a_job_decides = 'offered a job, decides'


class ResumeStatus(enum.Enum):
    in_work = 'in_work'
    screening = 'screening'
    interview = 'interview'
    rejected = 'rejected'
    offer = 'offer'


class EducationDegree(enum.Enum):
    incomplete_primary = 'incomplete primary'
    primary = 'primary'
    secondary = 'secondary'
    incomplete_secondary = 'incomplete secondary'
    secondary_vocational = 'secondary vocational'
    incomplete_higher = 'incomplete higher'
    higher = 'higher'
    bachelor = 'bachelor'
    master = 'master'
    phd = 'phd'


# Models
class Resume(Base):
    __tablename__ = "resume"
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidate.id", ondelete="CASCADE"), nullable=False)
    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancy.id", ondelete="CASCADE"), nullable=False)
    resume_status: Mapped[ResumeStatus]
    rating: Mapped[int | None] = None
    job_title: Mapped[str]
    expected_salary: Mapped[int | None]
    interest_in_job: Mapped[InterestInJob | None]
    skills: Mapped[list[str] | None] = mapped_column(ARRAY(String(255)))
    ready_to_relocate: Mapped[bool | None]
    ready_for_business_trips: Mapped[bool | None]

    # relationships
    vacancy = relationship("Vacancy", back_populates="resumes")
    candidate = relationship("Candidate", back_populates="resume", cascade="all, delete", lazy="joined")
    educations = relationship("Education", back_populates="resume", cascade="all, delete-orphan", lazy="joined")
    experiences = relationship("WorkExperience", back_populates="resume", cascade="all, delete-orphan", lazy="joined")

    def __doc__(self):
        return f"Resume({self.id}) {self.job_title}"
    
    def __str__(self):
        return f"({self.id}) {self.job_title}"


class Education(Base):
    __tablename__ = "education"
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey('resume.id', ondelete="CASCADE"), nullable=False)
    educational_institution: Mapped[str]
    degree: Mapped[EducationDegree]
    year: Mapped[int]
    specialization: Mapped[str]

    # relationships
    resume = relationship("Resume", back_populates="educations")

    def __doc__(self):
        return f"Education({self.id}) {self.educational_institution}"
    
    def __str__(self):
        return f"({self.id}) {self.educational_institution}"


class WorkExperience(Base):
    __tablename__ = "work_experience"
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey('resume.id', ondelete="CASCADE"), nullable=False)
    company: Mapped[str]
    start_date: Mapped[date]
    end_date: Mapped[date]
    description: Mapped[str]

    # relationships
    resume = relationship("Resume", back_populates="experiences")

    def __doc__(self):
        return f"WorkExperience({self.id}) {self.company}"
    
    def __str__(self):
        return f"({self.id}) {self.company}"


class Candidate(Base):
    __tablename__ = "candidate"
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str | None]
    age: Mapped[int | None]
    gender: Mapped[Gender | None]
    city: Mapped[str | None]
    about: Mapped[str | None]
    telegram: Mapped[str | None] = mapped_column(String, nullable=True)
    whatsapp: Mapped[str | None] = mapped_column(String, nullable=True)
    linkedin: Mapped[str | None] = mapped_column(String, nullable=True)
    github: Mapped[str | None] = mapped_column(String, nullable=True)
    email: Mapped[str | None] = mapped_column(String, nullable=True)
    phone_number: Mapped[str | None] = mapped_column(String, nullable=True)
    profile_picture_url: Mapped[str | None] = mapped_column(String, nullable=True)

    # relationships
    resume = relationship("Resume", back_populates="candidate")

    def __doc__(self):
        return f"Candidate({self.id}) {self.first_name} {self.last_name}"
    
    def __str__(self):
        return f"({self.id}) {self.first_name} {self.last_name}"

