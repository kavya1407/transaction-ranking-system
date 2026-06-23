from sqlalchemy.orm import Session
from datetime import datetime
from . import models, schemas

def create_transaction(db: Session, tx: schemas.TransactionCreate):
    try:
        existing = db.query(models.Transaction).filter(
            models.Transaction.idempotency_key == tx.idempotency_key
        ).first()

        if existing:
            return {
                "message": "Duplicate transaction ignored",
                "transaction_id": existing.id
            }

        stats = db.query(models.UserStats).filter(
            models.UserStats.user_id == tx.user_id
        ).first()

        if not stats:
            stats = models.UserStats(
                user_id=tx.user_id,
                total_amount=0,
                total_transaction_volume=0,
                transaction_count=0
            )
            db.add(stats)

        if tx.type == "debit" and stats.total_amount < tx.amount:
            raise ValueError("Insufficient balance for debit transaction")

        new_tx = models.Transaction(
            user_id=tx.user_id,
            amount=tx.amount,
            type=tx.type,
            idempotency_key=tx.idempotency_key
        )
        db.add(new_tx)

        # Update current balance / net amount
        if tx.type == "credit":
            stats.total_amount += tx.amount
        else:
            stats.total_amount -= tx.amount

        # Update total transaction volume
        stats.total_transaction_volume += tx.amount

        stats.transaction_count += 1
        stats.last_transaction_time = datetime.utcnow()

        db.commit()
        db.refresh(new_tx)

        return {
            "message": "Transaction successful",
            "transaction_id": new_tx.id
        }

    except Exception as e:
        db.rollback()
        raise e


def get_user_summary(db: Session, user_id: str):
    stats = db.query(models.UserStats).filter(
        models.UserStats.user_id == user_id
    ).first()

    if not stats:
        return None

    avg = 0
    if stats.transaction_count > 0:
        avg = stats.total_transaction_volume / stats.transaction_count

    return {
        "user_id": stats.user_id,
        "total_amount": stats.total_amount,
        "transaction_count": stats.transaction_count,
        "average_transaction": round(avg, 2)
    }