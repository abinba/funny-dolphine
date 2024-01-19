from src.db.models import Review
from src.repo.base import BaseRepo
from src.schemas.review import ReviewSchema

class ReviewRepo(BaseRepo):
    model = Review
    validation_schema = ReviewSchema
