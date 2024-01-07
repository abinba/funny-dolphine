from src.db.models import Category
from src.repo.base import BaseRepo
from src.schemas.category import CategorySchema


class CategoryRepo(BaseRepo):
    model = Category
    validation_schema = CategorySchema
