from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.repository.base import BaseRepository
from app.infrastructure.db.models import TransactionLog
from app.core.models import dto


class TransactionLogRepository(BaseRepository[TransactionLog]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(TransactionLog, session)

    async def get_by_id(self, id: int) -> dto.TransactionLog:
        return (await self._get_by_id(id)).to_dto()
    
    async def create(self, transaction: dto.TransactionLog) -> dto.TransactionLog:
        transaction_db = TransactionLog(
            idempotency_key=transaction.idempotency_key,
            type=transaction.type
            
        )
        self._save(transaction_db)
        await self._flush(transaction_db)
        return transaction_db.to_dto()
