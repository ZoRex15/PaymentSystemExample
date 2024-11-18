from typing import Optional

from decimal import Decimal

from pydantic import BaseModel

from app.core.models.enum import WithdrawalOperationStatus, ReplenishmentOperationStatus


class CounteragentBalance(BaseModel):
    counteragent_id: int
    balance: Decimal

class ReplenishmentBalanceResult(BaseModel):
    status: ReplenishmentOperationStatus
    error_description: Optional[str] = None

class WithdrawalBalanceResult(BaseModel):
    status: WithdrawalOperationStatus
    error_description: Optional[str] = None