from pydantic import BaseModel, field_validator
from typing import Literal

class TransactionCreate(BaseModel):
    user_id: str
    amount: float
    type: Literal["credit", "debit"]
    idempotency_key: str

    @field_validator("user_id")
    @classmethod
    def validate_user_id(cls, v):
        if not v.strip():
            raise ValueError("User ID cannot be empty")
        return v

    @field_validator("idempotency_key")
    @classmethod
    def validate_idempotency_key(cls, v):
        if not v.strip():
            raise ValueError("Idempotency key cannot be empty")
        return v

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError("Amount must be greater than 0")
        if v > 10000:
            raise ValueError("Amount exceeds allowed limit")
        return v

class TransactionResponse(BaseModel):
    message: str
    transaction_id: int | None = None

class SummaryResponse(BaseModel):
    user_id: str
    total_amount: float
    transaction_count: int
    average_transaction: float

class RankingItem(BaseModel):
    user_id: str
    score: float
    rank: int