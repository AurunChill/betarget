import asyncio

from typing import AsyncGenerator, Generator
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from config import settings
from main import app

api_prefix = "/api/v1"

test_urls = {
    "auth": {
        "register": "/auth/register",
        "login": "/auth/login",
        "logout": "/auth/logout",
        "forgot_password": "/auth/forgot-password",
        "reset_password": "/auth/reset-password",
        "ask_verification": "/auth/ask_verification",
        "verify_account": "/auth/verify-account",
    },
    "user": {
        "update": f"{api_prefix}/user/",
        "delete": f"{api_prefix}/user/",
        "update_profile_image": f"{api_prefix}/user/update_profile_image",
        "get_user_exists": f"{api_prefix}/user/is_exists",
        "my_data": f"{api_prefix}/user/my_data",
    },
    "vacancy": {
        "get_all_vacancies": f"{api_prefix}/vacancy/",
        "create_user_vacancy": f"{api_prefix}/vacancy/",
        "update_user_vacancy": f"{api_prefix}/vacancy/",
        "get_user_vacancy": f"{api_prefix}/vacancy/",
        "delete_user_vacancy": f"{api_prefix}/vacancy/",
    },
    "resume": {
        "get_all_resumes": f"{api_prefix}/resume/",
        "create_user_resume": f"{api_prefix}/resume/",
        "update_user_resume": f"{api_prefix}/resume/",
        "get_user_resume": f"{api_prefix}/resume/",
        "delete_user_resume": f"{api_prefix}/resume/",
    },
    "sse": {
        "get_sse": f"{api_prefix}/sse/events",
    },
}


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def user_data() -> dict:
    return {
        "username": "test_user",
        "email": "test@ex.com",
        "password": "SuperUsername1233",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "telegram": "https://example.com/",
        "whatsapp": "https://example.com/",
        "linkedin": "https://example.com/",
        "phone_number": "+77777777777",
        "subscription_type": "free",
        "profile_picture_url": "https://example.com/",
    }


@pytest.fixture
async def vacancy_data() -> dict:
    return {
        "job_title": "string",
        "city": "string",
        "company": "string",
        "experience": "no experience",
        "work_format": "in office",
        "salary": 25000,
        "education": "phd",
        "employment_type": "full_time",
        "skills": ["string"],
        "description": "string",
    }


@pytest.fixture
async def resume_data() -> dict:
    return {
        "resume_status": "in_work",
        "rating": 5,
        "job_title": "string",
        "expected_salary": 15000,
        "interest_in_job": "looking for job",
        "skills": ["string"],
        "ready_to_relocate": True,
        "ready_for_business_trips": True,
        "candidate": {
            "first_name": "string",
            "last_name": "string",
            "age": 25,
            "gender": "male",
            "city": "string",
            "about": "string",
            "telegram": "https://example.com/",
            "whatsapp": "https://example.com/",
            "linkedin": "https://example.com/",
            "github": "https://example.com/",
            "email": "user@example.com",
            "phone_number": "+77777777777",
            "profile_picture_url": "https://example.com/",
        },
        "educations": [
            {
                "educational_institution": "string",
                "year": "2024",
                "degree": "incomplete primary",
                "specialization": "string",
            }
        ],
        "experiences": [
            {
                "company": "string",
                "start_date": "2024-07-22",
                "end_date": "2024-07-22",
                "description": "string",
            }
        ],
    }


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url=settings.test.BASE_URL
    ) as client:
        yield client


@pytest_asyncio.fixture
async def auth_async_client(async_client: AsyncClient, user_data: dict) -> AsyncClient:
    response_data = await async_client.post(
        url=test_urls["auth"].get("register"),
        json={
            "username": user_data.get("username"),
            "email": user_data.get("email"),
            "password": user_data.get("password"),
        },
    )
    login_response = await async_client.post(
        url=test_urls["auth"].get("login"),
        data={
            "username": user_data.get("email"),
            "password": user_data.get("password"),
        },
    )
    async_client.cookies = {
        "bonds": login_response.headers.get("set-cookie").split(";")[0][6:],
        "user_id": response_data.json().get("id"),
    }
    return async_client
