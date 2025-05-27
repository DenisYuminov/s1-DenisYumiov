from recipe.schemas import CreateRecipe, UpdateRecipe
from config import SECRET_AUTH
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import select, insert, update, delete, join
from db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from auth.base_config import current_user
from recipe.models import recipe, tag, ingredient, method, recipe_method, recipe_ingredient, recipe_tag
from config import settings
router = APIRouter(
    prefix=f"{settings.API_PATH}/recipes",
    tags=["Recipes"]
)
reset_password_token_secret = SECRET_AUTH
verification_token_secret = SECRET_AUTH


@router.post("/create")
async def add_recipe(
        new_recipe: CreateRecipe,
        session: AsyncSession = Depends(get_async_session),
        user=Depends(current_user)
):
    """

    :param new_recipe: schema for create recipe
    :param session: database session
    :param user: current_user
    :return:
    """
    # Вставка данных в таблицу tags
    tag_ids = []
    for tag_data in new_recipe.tags:
        tag_stmt = insert(tag).values(name=tag_data.name)
        tag_result = await session.execute(tag_stmt)
        tag_ids.append(tag_result.inserted_primary_key[0])

    # Вставка данных в таблицу ingredients
    ingredient_ids = []
    for ingredient_data in new_recipe.ingredients:
        ingredient_stmt = insert(ingredient).values(name=ingredient_data.name)
        ingredient_result = await session.execute(ingredient_stmt)
        ingredient_ids.append(ingredient_result.inserted_primary_key[0])

    # Вставка данных в таблицу method
    method_ids = []
    for method_data in new_recipe.method:
        method_stmt = insert(method).values(text=method_data.text)
        method_result = await session.execute(method_stmt)
        method_ids.append(method_result.inserted_primary_key[0])

    # Вставка данных в таблицу recipe (без связанных данных)
    recipe_stmt = insert(recipe).values(
        user_id=user.id,
        title=new_recipe.title,
        image=new_recipe.image,
        time_to_cook=new_recipe.time_to_cook,
        time_to_prepare=new_recipe.time_to_prepare,
        description=new_recipe.description,
        date=new_recipe.date,
        kcal=new_recipe.kcal,
        fat=new_recipe.fat,
        saturates=new_recipe.saturates,
        protein=new_recipe.protein
    )
    recipe_result = await session.execute(recipe_stmt)
    recipe_id = recipe_result.inserted_primary_key[0]

    # Связывание идентификаторов с рецептом в таблицах-связках
    for tag_id in tag_ids:
        recipe_tag_stmt = insert(recipe_tag).values(recipe_id=recipe_id, tag_id=tag_id)
        await session.execute(recipe_tag_stmt)

    for ingredient_id in ingredient_ids:
        recipe_ingredient_stmt = insert(recipe_ingredient).values(recipe_id=recipe_id, ingredient_id=ingredient_id)
        await session.execute(recipe_ingredient_stmt)

    for method_id in method_ids:
        recipe_method_stmt = insert(recipe_method).values(recipe_id=recipe_id, method_id=method_id)
        await session.execute(recipe_method_stmt)

    await session.commit()
    return {"status": "success"}


@router.get("/{recipe_id}")
async def get_recipe(recipe_id: int, session: AsyncSession = Depends(get_async_session)):
    """

    :param recipe_id: int
    :param session: database session
    :return:
    """
    recipe_query = select(recipe).where(recipe.c.id == recipe_id)

    ingredient_query = select(ingredient).select_from(
        join(recipe_ingredient, ingredient, recipe_ingredient.c.ingredient_id == ingredient.c.id)
    ).where(recipe_ingredient.c.recipe_id == recipe_id)

    tag_query = select(tag).select_from(
        join(recipe_tag, tag, recipe_tag.c.tag_id == tag.c.id)
    ).where(recipe_tag.c.recipe_id == recipe_id)

    method_query = select(method).select_from(
        join(recipe_method, method, recipe_method.c.method_id == method.c.id)
    ).where(recipe_method.c.recipe_id == recipe_id)

    recipe_result = await session.execute(recipe_query)
    db_recipe = recipe_result.fetchone()

    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    ingredient_result = await session.execute(ingredient_query)
    db_ingredients = ingredient_result.fetchall()

    tag_result = await session.execute(tag_query)
    db_tags = tag_result.fetchall()

    method_result = await session.execute(method_query)
    db_methods = method_result.fetchall()

    recipe_dict = {
        "id": db_recipe[0],
        "user_id": db_recipe[1],
        "image": db_recipe[2],
        "title": db_recipe[3],
        "time_to_cook": db_recipe[4],
        "time_to_prepare": db_recipe[5],
        "description": db_recipe[6],
        "date": db_recipe[7],
        "kcal": db_recipe[8],
        "fat": db_recipe[9],
        "saturates": db_recipe[10],
        "protein": db_recipe[11],
        "ingredients": [{k: db_ingredient[i]
                         for i, k in enumerate(ingredient.c.keys())}
                        for db_ingredient in db_ingredients],
        "tags": [{k: db_tag[i] for i, k in enumerate(tag.c.keys())} for db_tag in db_tags],
        "methods": [
    {
        "step": db_method.step,
        "text": db_method.text,
    }
        for db_method in db_methods
        ],
    }
    print(recipe_dict)
    return {
        "status": "success",
        "data": recipe_dict,
        "details": None
    }


@router.put("/{recipe_id}")
async def update_recipe(
    recipe_id: int,
    updated_recipe: UpdateRecipe,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(current_user)
):
    """

    :param recipe_id: int
    :param updated_recipe: UpdateRecipe
    :param session: Depends(get_async_session)
    :param user: current_user
    :return:
    """
    try:
        recipe_stmt = update(recipe).where(recipe.c.id == recipe_id).values(
            title=updated_recipe.title,
            image=updated_recipe.image,
            time_to_cook=updated_recipe.time_to_cook,
            time_to_prepare=updated_recipe.time_to_prepare,
            description=updated_recipe.description,
            kcal=updated_recipe.kcal,
            fat=updated_recipe.fat,
            saturates=updated_recipe.saturates,
            protein=updated_recipe.protein
        ).where(recipe.c.user_id == user.id)

        result = await session.execute(recipe_stmt)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Recipe not found or user is not the owner")

        await session.commit()
        return {
            "status": "success",
            "data": recipe_stmt,
            "details": None
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        }
    )


@router.delete("/{recipe_id}")
async def delete_recipe(
        recipe_id: int,
        session: AsyncSession = Depends(get_async_session),
        user=Depends(current_user)
):
    """

    :param recipe_id: int
    :param session: Depends(get_async_session)
    :param user: current_user
    :return:
    """
    recipe_stmt = delete(recipe).where(recipe.c.id == recipe_id).where(recipe.c.user_id == user.id)
    result = await session.execute(recipe_stmt)

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Recipe not found or user is not the owner")

    await session.commit()
    return {"status": "success"}


@router.get("")
async def get_all_recipes(session: AsyncSession = Depends(get_async_session)):
    """
    :param session: get_async_session
    :return:
    """
    try:
        recipe_stmt = select(recipe)
        recipe_results = await session.execute(recipe_stmt)
        recipes = recipe_results.all()
        return {
            "status": "success",
            "data": recipes,
            "details": None
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        }
    )