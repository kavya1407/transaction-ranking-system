from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .db import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    idempotency_key = Column(String, unique=True, nullable=False, index=True)

class UserStats(Base):
    __tablename__ = "user_stats"

    user_id = Column(String, primary_key=True, index=True)
    total_amount = Column(Float, default=0)   # current balance / net amount
    total_transaction_volume = Column(Float, default=0)   # NEW
    transaction_count = Column(Integer, default=0)
    last_transaction_time = Column(DateTime, nullable=True)