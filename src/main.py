from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate
from recipe.router import router as router_recipe
from pages.router import router as pages_router
from chat.router import router as chat_router
from config import settings
from http.client import HTTPException
from auth.manager import get_user_manager


app = FastAPI(
    title="Meal Helper"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix=f"{settings.API_PATH}/auth/jwt",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix=f"{settings.API_PATH}/auth",
    tags=["Auth"],
)

app.include_router(router_recipe)
app.include_router(pages_router)
app.include_router(chat_router)



templates = Jinja2Templates(directory="templates")
