from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.repository import (
    TransactionLogRepository,
    PostingRepository
)


class HolderRepository:
    def __init__(self, session: AsyncSession):
        self.transaction_log = TransactionLogRepository(session)
        self.posting = PostingRepository(session)
        
