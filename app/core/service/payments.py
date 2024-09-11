from logging import getLogger
from typing import Final
from decimal import Decimal
from uuid import UUID

from sqlalchemy.exc import IntegrityError

from app.core.interfaces.repository.posting import (
    PostingCreateReplenishmentOperation,
    PostingCreateWithdrawalOperation, 
    PostingCreate
)
from app.core.interfaces.repository.transaction_log import TransactionLogCreate

from app.core.models import dto
from app.core.models.enum import TransactionLogType, WithdrawalOperationStatus, ReplenishmentOperationStatus

logger = getLogger(__name__)

CASH_BOOK: Final = 1

async def _create_posting(
    repository: PostingCreate, 
    posting: dto.Posting
) -> dto.Posting:
    result = await repository.create(posting)
    return result

async def _create_transaction_log(
    repository: TransactionLogCreate, 
    transaction_log: dto.TransactionLog
) -> dto.TransactionLog:
    result = await repository.create(transaction_log)
    return result


async def withdrawal_balance(
    transaction_log_repository: TransactionLogCreate,
    posting_repository: PostingCreateWithdrawalOperation,
    counteragent_id: int,
    amount: Decimal,
    IK: UUID
) -> WithdrawalOperationStatus:
    try:
        counteragent_balance = await posting_repository.calculate_counteragent_balance(
            counteragent_id=counteragent_id
        )
        if counteragent_balance >= amount:
            transaction_log = await _create_transaction_log(
                repository=transaction_log_repository,
                transaction_log=dto.TransactionLog(
                    type=TransactionLogType.BALANCE_WITHDRAWAL,
                    idempotency_key=IK
                )
            )
            await _create_posting(
                repository=posting_repository,
                posting=dto.Posting(
                    counteragent_id=CASH_BOOK,
                    transaction_id=transaction_log.id,
                    amount=amount
                )
            )
            await _create_posting(
                repository=posting_repository,
                posting=dto.Posting(
                    counteragent_id=counteragent_id,
                    transaction_id=transaction_log.id,
                    amount=-amount
                )
            )
            await transaction_log_repository.commit()
            return WithdrawalOperationStatus.SUCCESSFULLY
        else:
            return WithdrawalOperationStatus.NOT_ENOUGH_RESOURCES
    except IntegrityError as error:
        await transaction_log_repository.rollback()
        return WithdrawalOperationStatus.SUCCESSFULLY
    except Exception as error:
        logger.error("Withdrawal operation error", error)
        return WithdrawalOperationStatus.FAILURE
    

async def replenishment_balance(
    transaction_log_repository: TransactionLogCreate,
    posting_repository: PostingCreateReplenishmentOperation,
    counteragent_id: int,
    amount: Decimal,
    IK: UUID
) -> ReplenishmentOperationStatus:
    try:
        transaction_log = await _create_transaction_log(
            repository=transaction_log_repository,
            transaction_log=dto.TransactionLog(
                type=TransactionLogType.BALANCE_REPLENISHMENT,
                idempotency_key=IK
            )
        )
        await _create_posting(
            repository=posting_repository,
            posting=dto.Posting(
                counteragent_id=CASH_BOOK,
                transaction_id=transaction_log.id,
                amount=-amount
            )
        )
        await _create_posting(
            repository=posting_repository,
            posting=dto.Posting(
                counteragent_id=counteragent_id,
                transaction_id=transaction_log.id,
                amount=amount
            )
        )
        await posting_repository.commit()
        return ReplenishmentOperationStatus.SUCCESSFULLY
    except IntegrityError as error:
        await transaction_log_repository.rollback()
        return ReplenishmentOperationStatus.SUCCESSFULLY
    except Exception as error:
        await transaction_log_repository.rollback()
        logger.error("Replenishment balance error", error)
        return ReplenishmentOperationStatus.FAILURE
