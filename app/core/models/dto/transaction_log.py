from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.core.models.enum import TransactionLogType


class TransactionLog(BaseModel):
    type: TransactionLogType
    idempotency_key: UUID

    create_at: datetime | None = None
    id: int | None = None