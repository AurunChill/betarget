import os

import pytest
from httpx import AsyncClient

from conftest import test_urls
from s3_storage import s3_client
from logger import test_logger as logger
from config import PROJECT_PATH, settings


@pytest.mark.asyncio
async def test_update_user(auth_async_client: AsyncClient, user_data: dict):
    init_user_data = user_data.copy()
    new_data = init_user_data.copy()
    del new_data["profile_picture_url"]
    new_data["phone_number"] = "+79998887766"
    new_data["linkedin"] = "https://linkedin.com/"
    logger.info(f"User data {user_data}")
    response = await auth_async_client.put(url=test_urls["user"].get("update"), json=new_data)
    response_data = response.json()
    logger.info(f"Response data {response_data}")
    response_phone = response_data.get("phone_number")
    response_linkedin = response_data.get("linkedin")
    assert response.status_code in [200, 204] and response_phone == "tel:+7-999-888-77-66" and response_linkedin == "https://linkedin.com/"


@pytest.mark.asyncio
async def test_update_unsuccessfully(auth_async_client: AsyncClient, user_data: dict):
    response = await auth_async_client.put(url=test_urls["user"].get("update"), json={})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_profile_image_success(auth_async_client: AsyncClient):
    filename = "test_image.png"
    test_image_path = PROJECT_PATH / "src" / "tests" / "img" / filename

    if not os.path.exists(test_image_path):
        pytest.fail("Test image file does not exist")

    with open(test_image_path, "rb") as image_file:
        files = {"profile_picture": ("test_image.png", image_file, "image/png")}
        response = await auth_async_client.put(test_urls["user"].get("update_profile_image"), files=files)
        response_data = response.json()
    
    logger.info(f"Update profile image response data {response_data}")
    test_url = settings.s3.S3_PUBLIC_DOMAIN + "/" + "profile-pictures/test_user/" + filename
    assert response.status_code == 200 and response_data == test_url
    await s3_client.delete_file(filename)
    


@pytest.mark.asyncio
async def test_update_profile_image_unsuccessful(auth_async_client: AsyncClient):
    response = await auth_async_client.put(test_urls["user"].get("update_profile_image"), files={})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_user(auth_async_client: AsyncClient, user_data: dict):
    response = await auth_async_client.delete(url=test_urls["user"].get("delete"))
    assert response.status_code in [200, 204]


@pytest.mark.asyncio
async def test_check_user_exists_empty(auth_async_client: AsyncClient):
    response = await auth_async_client.get(url=test_urls["user"].get("get_user_exists"))
    assert response.status_code == 200
    assert response.json() == {}


@pytest.mark.asyncio
async def test_check_user_exists_email(auth_async_client: AsyncClient):
    email = "test@example.com"
    response = await auth_async_client.get(url=test_urls["user"].get("get_user_exists"), params={"email": email})
    assert response.status_code == 200
    assert "is_exists_by_email" in response.json()


@pytest.mark.asyncio
async def test_check_user_exists_username(auth_async_client: AsyncClient):
    username = "testuser"
    response = await auth_async_client.get(url=test_urls["user"].get("get_user_exists"), params={"username": username})
    assert response.status_code == 200
    assert "is_exists_by_username" in response.json()


@pytest.mark.asyncio
async def test_check_user_exists_both(auth_async_client: AsyncClient):
    email = "test@example.com"
    username = "testuser"
    response = await auth_async_client.get(url=test_urls["user"].get("get_user_exists"), params={"email": email, "username": username})
    assert response.status_code == 200
    assert "is_exists_by_email" in response.json()
    assert "is_exists_by_username" in response.json()


@pytest.mark.asyncio
async def test_get_my_data_successfull(auth_async_client: AsyncClient, user_data):
    response = await auth_async_client.get(url=test_urls["user"].get("my_data"))
    response_data = response.json()
    assert response.status_code == 200 and response_data.get("username") == user_data.get("username")


@pytest.mark.asyncio
async def test_get_my_data_unsuccessfull(async_client: AsyncClient):
    response = await async_client.get(url=test_urls["user"].get("my_data"))
    assert response.status_code == 401