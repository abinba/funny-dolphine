from sqlalchemy import select

from src.db.models import UserShelf, Audiobook
from src.repo.base import BaseRepo
from src.schemas.audiobook import AudiobookSchema


class ShelfRepo(BaseRepo):
    model = UserShelf
    validation_schema = AudiobookSchema

    @classmethod
    async def create_or_update(cls, session, account_id, audiobook_id):
        query = select(cls.model).where(
            cls.model.account_id == account_id,
            cls.model.audiobook_id == audiobook_id,
        )
        result = await session.execute(query)
        shelf = result.scalar_one_or_none()

        if shelf is None:
            return await cls.create(
                session,
                account_id=account_id,
                audiobook_id=audiobook_id,
            )
        else:
            shelf.is_active = True
            await session.commit()
            return shelf

    @classmethod
    async def get_audiobooks(cls, session, account_id) -> list[AudiobookSchema]:
        query = select(cls.model.audiobook_id).where(
            cls.model.account_id == account_id, cls.model.is_active == True
        )
        result = await session.scalars(query)
        query = select(Audiobook).where(Audiobook.audiobook_id.in_(result.all()))
        audiobooks = await session.scalars(query)

        return [AudiobookSchema.model_validate(audiobook) for audiobook in audiobooks]

    @classmethod
    async def remove_from_shelf(cls, session, account_id, audiobook_id):
        query = select(cls.model).where(
            cls.model.account_id == account_id,
            cls.model.audiobook_id == audiobook_id,
            cls.model.is_active == True,
        )
        result = await session.execute(query)
        shelf = result.scalar_one()
        shelf.is_active = False
        await session.commit()
