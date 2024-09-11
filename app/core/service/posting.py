from decimal import Decimal

from app.core.interfaces.repository.posting import (
    PostingCalculateCounteragentBalance
)


async def calculate_counteragent_balance(
    repository: PostingCalculateCounteragentBalance,
    counteragent_id: int
) -> Decimal:
    return await repository.calculate_counteragent_balance(counteragent_id)
