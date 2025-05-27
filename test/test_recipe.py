from httpx import AsyncClient
from main import app
import pytest
from src.config import settings


@pytest.mark.asyncio
async def test_add_recipe():
    async with AsyncClient(app=app, base_url=f"{settings.API_PATH}") as client:
        response = await client.post("/recipes/create")
        assert response.status_code == 200
        # Add assertions for the expected response data

@pytest.mark.asyncio
async def test_get_recipe():
    async with AsyncClient(app=app, base_url=f"{settings.API_PATH}") as client:
        response = await client.get("/recipes/{recipe_id}")
        assert response.status_code == 200
        # Add assertions for the expected response data

@pytest.mark.asyncio
async def test_update_recipe():
    async with AsyncClient(app=app, base_url=f"{settings.API_PATH}") as client:
        response = await client.put("/recipes/{recipe_id}")
        assert response.status_code == 200
        # Add assertions for the expected response data

@pytest.mark.asyncio
async def test_delete_recipe():
    async with AsyncClient(app=app, base_url=f"{settings.API_PATH}") as client:
        response = await client.delete("/recipes/{recipe_id}")
        assert response.status_code == 200
        # Add assertions for the expected response data

@pytest.mark.asyncio
async def test_get_all_recipes():
    async with AsyncClient(app=app, base_url=f"{settings.API_PATH}") as client:
        response = await client.get("/recipes")
        assert response.status_code == 200
        # Add assertions for the expected response data
