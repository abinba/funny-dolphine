from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Chapter
from src.repo.base import BaseRepo
from src.schemas.chapter import ChapterTree, ChapterFlat


class ChapterRepo(BaseRepo):
    model = Chapter

    @classmethod
    async def all(
        cls,
        session: AsyncSession,
        audiobook_id: int = None,
        tree_structure: bool = False,
    ):
        query = select(cls.model)
        if audiobook_id:
            query = query.where(
                cls.model.audiobook_id == audiobook_id,
            )
        query = query.order_by(cls.model.parent_id.desc())

        result = await session.scalars(query)

        if tree_structure is False:
            return cls.get_flat_chapters(result)
        else:
            return cls.get_tree_chapters(result)

    @classmethod
    def get_flat_chapters(cls, result):
        results = []
        for row in result.unique().all():
            result_dict = {
                **row.__dict__,
                "children_ids": [child.chapter_id for child in row.children],
            }
            del result_dict["children"]
            results.append(result_dict)
        return [ChapterFlat.model_validate(item) for item in results]

    @classmethod
    def get_tree_chapters(cls, result):
        results = []
        for row in result.unique().all():
            if row.parent_id is None:
                results.append(row)
        return [ChapterTree.model_validate(item) for item in results]
