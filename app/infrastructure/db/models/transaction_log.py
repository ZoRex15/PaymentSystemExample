from datetime import date

from sqlalchemy import BigInteger, Enum, UUID, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import DATE, TIMESTAMP

from app.infrastructure.db.models.base import Base
from app.core.models import dto
from app.core.models.enum import TransactionLogType


class TransactionLog(Base):
    __tablename__ = 'TransactionLogs'
    __table_args__ = (
        UniqueConstraint(
            'type', 
            'idempotency_key', 
            name='type_and_ik',
            info={'description':'TBC'}
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    type: Mapped[str] = mapped_column(Enum(TransactionLogType), nullable=False)
    create_at: Mapped[date] = mapped_column(TIMESTAMP(timezone=True), default=func.now())
    idempotency_key: Mapped[UUID] = mapped_column(UUID, nullable=False) 

    postings = relationship(
        'Posting',
        cascade='all, delete-orphan',
        back_populates='transaction_log'
    )

    def __repr__(self) -> str:
        return (
            'TransactionLogModel('
            f'id={self.id}, '
            f'type={self.type}, '
            f'create_at={self.create_at}, '
            f'idempotency_key={self.idempotency_key})'
        )
    
    def to_dto(self) -> dto.TransactionLog:
        return dto.TransactionLog(
            id=self.id,
            type=self.type,
            create_at=self.create_at,
            idempotency_key=self.idempotency_key
        )