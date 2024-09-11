from typing import Protocol
from decimal import Decimal
from .base import UoW

from app.core.models import dto


class PostingCreateReplenishmentOperation(UoW, Protocol):
    async def create(self, posting: dto.Posting) -> dto.Posting:
        raise NotImplementedError
    
class PostingCreate(UoW, Protocol):
    async def create(self, posting: dto.Posting) -> dto.Posting:
        raise NotImplementedError

class PostingCalculateCounteragentBalance(UoW, Protocol):
    async def calculate_counteragent_balance(
        self, 
        counteragent_id: int
    ) -> Decimal:
        raise NotImplementedError
        
class PostingCreateWithdrawalOperation(UoW, Protocol):
    async def create(self, posting: dto.Posting) -> dto.Posting:
        raise NotImplementedError
    
    async def calculate_counteragent_balance(
        self, 
        counteragent_id: int
    ) -> Decimal:
        raise NotImplementedError
