from faststream.nats import NatsRouter
from faststream.nats.annotations import NatsBroker, NatsMessage

from dishka import FromDishka

from app.infrastructure.db import HolderRepository
from app.core.models.messages.incoming_messages import (
    CounteragentGetBalance
)
from app.core.models.messages.outgoing_messages import (
    CounteragentBalance
)
from app.core.service.posting import calculate_counteragent_balance

router = NatsRouter()

@router.subscriber('counteragent.balance')
async def get_counteragent_balance(
    msg: CounteragentGetBalance,
    nats_msg: NatsMessage,
    broker: NatsBroker,
    repository: FromDishka[HolderRepository]
) -> CounteragentBalance:
    counteragent_balance = await calculate_counteragent_balance(
        repository.posting,
        msg.counteragent_id
    )
    return CounteragentBalance(
        balance=counteragent_balance,
        counteragent_id=msg.counteragent_id
    )
