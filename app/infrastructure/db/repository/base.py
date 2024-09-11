from typing import Generic, TypeVar

from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, ScalarResult
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.interfaces import ORMOption

from app.infrastructure.db.models.base import Base

Model = TypeVar('Model', bound=Base, covariant=True, contravariant=False)


class BaseRepository(Generic[Model]):
    def __init__(self, model: type[Model], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def _get_by_id(
        self,
        id: int,
        options: Sequence[ORMOption] | None = None,
        populate_existing: bool = False
    ) -> Model:
        result = await self.session.get(
            self.model,
            id,
            options=options,
            populate_existing=populate_existing
        )
        if result is None:
            raise NoResultFound
        return result

    async def _get_all(self, options: Sequence[ORMOption] = ()) -> Sequence[Model]:
        result: ScalarResult[Model] = await self.session.scalars(
            select(self.model).options(*options)
        )
        return result.all()
    
    async def delete(self, obj: Model) -> None:
        await self.session.delete(obj)

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def _flush(self, *objs: Base) -> None:
        await self.session.flush(objs) 

    def _save(self, obj: Base) -> None:
        self.session.add(obj)
         

    