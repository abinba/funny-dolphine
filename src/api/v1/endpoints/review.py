from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import authorize_user
from src.db import get_async_session
from src.repo.review import ReviewRepo
from src.schemas.review import ReviewSchema

router = APIRouter()

@router.get("/", response_model=list[ReviewSchema])
async def get_reviews(
        request: Request,
        session: AsyncSession = Depends(get_async_session),
):
    auth_header = request.headers.get("Authorization")
    authorize_user(auth_header)
    return await ReviewRepo.all(session)


# @router.get("/{category_id}", response_model=ReviewSchema)
# async def get_categories(
#         request: Request,
#         category_id: int,
#         session: AsyncSession = Depends(get_async_session),
# ):
#     auth_header = request.headers.get("Authorization")
#     authorize_user(auth_header)
#     return await ReviewRepo.get(session, category_id=category_id)
