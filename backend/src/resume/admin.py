from sqladmin import ModelView
from resume.models import (
    Resume, Candidate, Gender,
    InterestInJob, ResumeStatus, Education,
    EducationDegree, WorkExperience
)


class ResumeAdmin(ModelView, model=Resume):
    name = "Resume"
    name_plural = "Resumes"
    column_list = [
        "id",
        "resume_status",
        "rating",
        "job_title",
        "expected_salary",
        "interest_in_job",
        "skills",
        "experience",
        "ready_to_relocate",
        "ready_for_business_trips",
        "vacancy_id",
    ]
    column_labels = {
        "id": "ID",
        "resume_status": "Resume Status",
        "rating": "Rating",
        "job_title": "Job Title",
        "expected_salary": "Expected Salary",
        "interest_in_job": "Interest in Job",
        "skills": "Skills",
        "experience": "Experience",
        "ready_to_relocate": "Ready to Relocate",
        "ready_for_business_trips": "Ready for Business Trips",
        "vacancy_id": "Vacancy ID",
    }
    form_choices = {
        'resume_status': [
            (ResumeStatus.in_work.value, 'In Work'),
            (ResumeStatus.screening.value, 'Screening'),
            (ResumeStatus.interview.value, 'Interview'),
            (ResumeStatus.rejected.value, 'Rejected'),
            (ResumeStatus.offer.value, 'Offer')
        ],
        'interest_in_job': [
            (InterestInJob.looking_for_job.value, 'Looking for Job'),
            (InterestInJob.not_looking_for_a_job.value, 'Not Looking for a Job'),
            (InterestInJob.considers_proposals.value, 'Considers Proposals'),
            (InterestInJob.offered_a_job_decides.value, 'Offered a Job, Decides')
        ]
    }

class CandidateAdmin(ModelView, model=Candidate):
    name = "Candidate"
    name_plural = "Candidates"
    column_list = [
        "id",
        "first_name",
        "last_name",
        "age",
        "gender",
        "city",
        "about",
        "telegram",
        "whatsapp",
        "linkedin",
        "github",
        "email",
        "phone_number",
        "profile_picture_url",
    ]
    column_labels = {
        "id": "ID",
        "first_name": "First Name",
        "last_name": "Last Name",
        "age": "Age",
        "gender": "Gender",
        "city": "City",
        "about": "About",
        "telegram": "Telegram",
        "whatsapp": "WhatsApp",
        "linkedin": "LinkedIn",
        "github": "GitHub",
        "email": "Email",
        "phone_number": "Phone Number",
        "profile_picture_url": "Profile Picture URL",
    }
    form_choices = {
        'gender': [
            (Gender.male.value, 'Male'),
            (Gender.female.value, 'Female'),
            (Gender.other.value, 'Other')
        ]
    }

class EducationAdmin(ModelView, model=Education):
    name = "Education"
    name_plural = "Educations"
    column_list = [
        "id",
        "resume_id",
        "educational_institution",
        "year",
        "degree"
        "specialization",
    ]
    column_labels = {
        "id": "ID",
        "resume_id": "Resume ID",
        "educational_institution": "Educational Institution",
        "year": "Graduated Year",
        "degree": "Degree",
        "specialization": "Specialization",
    }
    form_choices = {
        'degree': [
            (EducationDegree.incomplete_primary.value, 'Incomplete Primary'),
            (EducationDegree.primary.value, 'Primary'),
            (EducationDegree.secondary.value, 'Secondary'),
            (EducationDegree.incomplete_secondary.value, 'Incomplete Secondary'),
            (EducationDegree.secondary_vocational.value, 'Secondary Vocational'),
            (EducationDegree.incomplete_higher.value, 'Incomplete Higher'),
            (EducationDegree.higher.value, 'Higher'),
            (EducationDegree.bachelor.value, 'Bachelor'),
            (EducationDegree.master.value, 'Master'),
            (EducationDegree.phd.value, 'PhD')
        ]
    }

class WorkExperienceAdmin(ModelView, model=WorkExperience):
    name = "WorkExperience"
    name_plural = "WorkExperiences"
    column_list = [
        "id",
        "resume_id",
        "company",
        "start_date",
        "end_date",
        "description",
    ]
    column_labels = {
        "id": "ID",
        "resume_id": "Resume ID",
        "company": "Company",
        "start_date": "Start Date",
        "end_date": "End Date",
        "description": "Description",
    }
