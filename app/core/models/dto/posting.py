from decimal import Decimal
from pydantic import BaseModel



class Posting(BaseModel):
    counteragent_id: int
    transaction_id: int
    amount: Decimal

    id: int | None = None