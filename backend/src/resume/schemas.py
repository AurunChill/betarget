from datetime import date

from pydantic import BaseModel, AnyHttpUrl, Field, EmailStr, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber

from resume.models import Gender, InterestInJob, ResumeStatus, EducationDegree


class CandidateCreate(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str | None = Field(None, max_length=50)
    age: int | None = Field(None, ge=0, le=130)
    gender: Gender | None
    city: str | None = Field(None, max_length=50)
    about: str | None = Field(None, max_length=2000)

    telegram: AnyHttpUrl | None = Field(None)
    whatsapp: AnyHttpUrl | None = Field(None)
    linkedin: AnyHttpUrl | None = Field(None)
    github: AnyHttpUrl | None = Field(None)
    email: EmailStr | None
    phone_number: PhoneNumber | None
    
    profile_picture_url: AnyHttpUrl | None = Field(None)

    @field_validator("telegram", "whatsapp", "linkedin", "github", "profile_picture_url")
    def validate_urls(cls, v):
        if v is None:
            return None
        return str(v)


class CandidateRead(BaseModel):
    id: int

    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str | None = Field(None, max_length=50)
    age: int | None = Field(None, ge=0, le=130)
    gender: Gender | None
    city: str | None = Field(None, max_length=50)
    about: str | None = Field(None, max_length=2000)

    telegram: AnyHttpUrl | None = Field(None)
    whatsapp: AnyHttpUrl | None = Field(None)
    linkedin: AnyHttpUrl | None = Field(None)
    github: AnyHttpUrl | None = Field(None)
    email: EmailStr | None
    phone_number: PhoneNumber | None
    
    profile_picture_url: AnyHttpUrl | None = Field(None)

    @field_validator("telegram", "whatsapp", "linkedin", "github", "profile_picture_url")
    def validate_urls(cls, v):
        if v is None:
            return None
        return str(v)


class CandidateUpdate(CandidateRead):
    pass


class EducationCreate(BaseModel):
    educational_institution: str = Field(..., max_length=255)
    year: int = Field(..., ge=1900)
    degree: EducationDegree
    specialization: str = Field(..., max_length=255)


class EducationRead(EducationCreate):
    id: int


class ExperienceCreate(BaseModel):
    company: str = Field(..., max_length=255)
    start_date: date
    end_date: date
    description: str = Field(..., max_length=2000)


class ExperienceRead(ExperienceCreate):
    id: int


class ResumeCreate(BaseModel):
    resume_status: ResumeStatus = 'in_work'
    rating: int | None = Field(None, ge=0, le=10)

    job_title: str = Field(..., min_length=1, max_length=60)
    expected_salary: int | None = Field(None, ge=0)
    interest_in_job: InterestInJob | None
    skills: list[str] | None = Field(None, max_length=20)
    ready_to_relocate: bool | None
    ready_for_business_trips: bool | None

    candidate: CandidateCreate = Field(...)
    educations: list[EducationCreate] | None = Field(None)
    experiences: list[ExperienceCreate] | None = Field(None)


class ResumeRead(BaseModel):
    id: int
    resume_status: ResumeStatus
    rating: int | None = Field(None, ge=0, le=10)
    
    job_title: str = Field(..., min_length=1, max_length=60)
    expected_salary: int | None = Field(None, ge=0)
    interest_in_job: InterestInJob | None
    skills: list[str] | None = Field(None, max_length=20)
    ready_to_relocate: bool | None
    ready_for_business_trips: bool | None

    candidate: CandidateRead = Field(...)
    educations: list[EducationRead] | None = Field(None)
    experiences: list[ExperienceRead] | None = Field(None)


class ResumeUpdate(ResumeRead):
    pass
