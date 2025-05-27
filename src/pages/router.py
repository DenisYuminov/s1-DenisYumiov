from http.client import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from wtforms import validators
from sqlalchemy.ext.asyncio import AsyncSession
from auth.base_config import current_user
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from recipe.router import get_all_recipes, get_recipe
from wtforms import Form, StringField, PasswordField, SubmitField
from auth.base_config import auth_backend
from auth.manager import get_user_manager
from fastapi.responses import RedirectResponse
from auth.utils import get_async_session
router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="templates")

security = HTTPBasic()


@router.get("/login", response_class=HTMLResponse)
def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login", response_class=HTMLResponse)
async def login(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password

    user_manager = get_user_manager()
    user_manager_instance = await next(user_manager)

    user = await user_manager_instance.authenticate(username, password)
    if user:
        token = await auth_backend.create_access_token(user)
        response = RedirectResponse(url="/main")
        response.set_cookie("access_token", token)
        return response

    raise HTTPException(status_code=401, detail="Invalid credentials")


@router.get("/main")
def get_search_page(request: Request, recipes=Depends(get_all_recipes)):
    """

    :param request: Request
    :param recipes: get_all_recipes
    :return:
    """
    return templates.TemplateResponse("main.html", {"request": request, "recipes": recipes["data"]})


@router.get("/recipes/{recipe_id}")
async def get_recipe_page(request: Request, recipe=Depends(get_recipe)):
    """
    :param request: Request
    :param recipes: get_all_recipes
    :return:
    """
    return templates.TemplateResponse("recipe.html", {
        "request": request,
        "recipe": recipe["data"],
        "current_user": Depends(current_user)
    })


@router.get("/create_recipe", response_class=HTMLResponse)
async def create_recipe(request: Request):
    """"
    :param request: Request
    :return:
    """
    return templates.TemplateResponse("create_recipe.html", {"request": request})


@router.post("/create_recipe")
async def add_recipe(
):
    return {"status": "success"}


@router.get("/chat")
def get_chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


