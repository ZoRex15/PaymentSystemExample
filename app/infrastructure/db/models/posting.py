from datetime import datetime
from decimal import Decimal

from sqlalchemy import BigInteger, ForeignKey, Text, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import TIMESTAMP

from app.infrastructure.db.models.base import Base
from app.core.models import dto


class Posting(Base):
    __tablename__ = 'Posting'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    counteragent_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    transaction_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('TransactionLogs.id'), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric, nullable=False)

    transaction_log = relationship(
        'TransactionLog',
        back_populates='postings',
        uselist=True,
        foreign_keys=[transaction_id]
    )

    def __repr__(self) -> str:
        return (
            'PostingModel('
            f'id={self.id}, '
            f'counteragent_id={self.counteragent_id}, '
            f'transaction_id={self.transaction_id}, '
            f'amount={self.amount})'
        )
    
    def to_dto(self) -> dto.Posting:
        return dto.Posting(
            id=self.id,
            counteragent_id=self.counteragent_id,
            transaction_id=self.transaction_id,
            amount=self.amount
        )