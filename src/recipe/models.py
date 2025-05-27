from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, MetaData, ForeignKey
from sqlalchemy.orm import relationship
from auth.models import User


metadata = MetaData()

ingredient = Table(
    "ingredient",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    extend_existing=True
)

tag = Table(
    "tag",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    extend_existing=True
)

method = Table(
    "method",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("step", Integer),
    Column("text", String, nullable=False),
    extend_existing=True

)

recipe = Table(
    "recipe",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey(User.id)),
    Column("image", String, nullable=False),
    Column("title", String, nullable=False),
    Column("time_to_cook", String, nullable=False),
    Column("time_to_prepare", String, nullable=False),
    Column("description", String, nullable=False),
    Column("date", TIMESTAMP),
    Column("kcal", Integer, nullable=False),
    Column("fat", Integer, nullable=False),
    Column("saturates", Integer, nullable=False),
    Column("protein", Integer, nullable=False),
    extend_existing=True
)
recipe_tag = Table(
    "recipe_tag",
    metadata,
    Column("recipe_id", Integer, ForeignKey(recipe.c.id), primary_key=True),
    Column("tag_id", Integer, ForeignKey(tag.c.id), primary_key=True),
    extend_existing=True
)

recipe_ingredient = Table(
    "recipe_ingredient",
    metadata,
    Column("recipe_id", Integer, ForeignKey(recipe.c.id), primary_key=True),
    Column("ingredient_id", Integer, ForeignKey(ingredient.c.id), primary_key=True),
    extend_existing=True
)

recipe_method = Table(
    "recipe_method",
    metadata,
    Column("recipe_id", Integer, ForeignKey(recipe.c.id), primary_key=True),
    Column("method_id", Integer, ForeignKey(method.c.id), primary_key=True),
    extend_existing=True
)

ingredient.recipes = relationship(
    "recipe",
    secondary=recipe_ingredient,
    back_populates="ingredients",
)

tag.recipes = relationship(
    "recipe",
    secondary=recipe_tag,
    back_populates="tags",
)

method.recipes = relationship(
    "recipe",
    secondary=recipe_method,
    back_populates="method",
)