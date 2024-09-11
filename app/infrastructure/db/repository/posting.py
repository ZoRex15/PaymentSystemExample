from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.infrastructure.db.repository.base import BaseRepository
from app.infrastructure.db.models import Posting
from app.core.models import dto


class PostingRepository(BaseRepository[Posting]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Posting, session)

    async def get_by_id(self, id: int) -> dto.Posting:
        return (await self._get_by_id(id)).to_dto()
    
    async def create(self, posting: dto.Posting) -> dto.Posting:
        posting_db = Posting(
            counteragent_id=posting.counteragent_id,
            transaction_id=posting.transaction_id,
            amount=posting.amount
        )
        self._save(posting_db)
        await self._flush(posting_db)
        return posting_db.to_dto()
    
    async def calculate_counteragent_balance(
        self, 
        counteragent_id: int
    ) -> Decimal:
        result = await self.session.execute(
            select(func.coalesce(func.sum(Posting.amount), 0))
            .where(Posting.counteragent_id == counteragent_id)
        )
        return Decimal(result.scalar())
   