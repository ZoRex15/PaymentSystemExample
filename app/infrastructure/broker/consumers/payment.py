from typing import Final

from faststream.nats import NatsRouter
from faststream.nats.annotations import NatsBroker, NatsMessage

from dishka import FromDishka

from app.infrastructure.db import HolderRepository

from app.core.models.messages.incoming_messages import (
    CounteragentBalanceReplenishment, 
    CounteragentBalanceWithdrawal
)
from app.core.models.messages.outgoing_messages import (
    ReplenishmentBalanceResult,
    WithdrawalBalanceResult
)
from app.core.service.payments import replenishment_balance, withdrawal_balance

IDEMPOTENCY_HEADER: Final = "X-Idempotency-Key"

router = NatsRouter()


@router.subscriber('counteragent.balance.replenishment')
async def counteragent_balance_replenishment(
    msg: CounteragentBalanceReplenishment,
    nats_msg: NatsMessage,
    broker: NatsBroker,
    repository: FromDishka[HolderRepository]
) -> ReplenishmentBalanceResult:
    result = await replenishment_balance(
        transaction_log_repository=repository.transaction_log,
        posting_repository=repository.posting,
        counteragent_id=msg.counteragent_id,
        amount=msg.amount,
        IK=nats_msg.headers.get(IDEMPOTENCY_HEADER)
    )
    return ReplenishmentBalanceResult(
        status=result
    )

@router.subscriber('counteragent.balance.withdrawal')
async def counteragent_balance_withdrawal(
    msg: CounteragentBalanceWithdrawal,
    nats_msg: NatsMessage,
    broker: NatsBroker,
    repository: FromDishka[HolderRepository]
) -> WithdrawalBalanceResult:
    result = await withdrawal_balance(
        transaction_log_repository=repository.transaction_log,
        posting_repository=repository.posting,
        counteragent_id=msg.counteragent_id,
        amount=msg.amount,
        IK=nats_msg.headers.get(IDEMPOTENCY_HEADER)
    )
    return WithdrawalBalanceResult(
        status=result
    )
   