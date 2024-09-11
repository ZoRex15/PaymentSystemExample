from decimal import Decimal

from pydantic import BaseModel


class CounteragentGetBalance(BaseModel):
    counteragent_id: int

class CounteragentBalanceReplenishment(BaseModel):
    counteragent_id: int
    amount: Decimal

class CounteragentBalanceWithdrawal(BaseModel):
    counteragent_id: int
    amount: Decimal