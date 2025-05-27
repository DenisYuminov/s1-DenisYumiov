from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class Ingredient(BaseModel):
    name: str


class Tag(BaseModel):
    name: str


class Method(BaseModel):
    step: int
    text: str


class CreateRecipe(BaseModel):
    user_id: int
    title: str
    image: str
    time_to_cook: str
    time_to_prepare: str
    description: str
    date: Optional[datetime] = datetime.now()
    kcal: int
    fat: int
    saturates: int
    protein: int
    ingredients: List[Ingredient]
    tags: List[Tag]
    method: List[Method]


class UpdateRecipe(BaseModel):
    title: Optional[str]
    image: Optional[str]
    time_to_cook: Optional[str]
    time_to_prepare: Optional[str]
    description: Optional[str]
    kcal: Optional[int]
    fat: Optional[int]
    saturates: Optional[int]
    protein: Optional[int]
    ingredients: Optional[List[Ingredient]]
    tags: Optional[List[Tag]]
    method: Optional[List[Method]]


class Recipe(BaseModel):
    id: int
    user_id: int
    title: str
    image: str
    time_to_cook: str
    time_to_prepare: str
    description: str
    date: Optional[datetime]
    kcal: int
    fat: int
    saturates: int
    protein: int
    ingredients: List[Ingredient]
    tags: List[Tag]
    method: List[Method]

