from typing import Protocol
from .base import UoW

from app.core.models import dto


class TransactionLogCreate(UoW, Protocol):
    async def create(self, transaction: dto.TransactionLog) -> dto.TransactionLog:
        raise NotImplementedError
    
# class TransactionLogGetByID(UoW, Protocol):
#     async def get_by_id(self, id: int) -> dto.TransactionLog:
#         raise NotImplementedError
