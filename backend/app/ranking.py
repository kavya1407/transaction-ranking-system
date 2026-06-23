from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from .models import UserStats

def calculate_score(stats):
    recency_bonus = 0

    if stats.last_transaction_time:
        if stats.last_transaction_time >= datetime.utcnow() - timedelta(days=1):
            recency_bonus = 10

    score = (
        (stats.total_amount * 0.5) +
        (min(stats.transaction_count, 20) * 2) +
        recency_bonus
    )
    return round(score, 2)

def get_rankings(db: Session):
    users = db.query(UserStats).all()

    ranking_list = []
    for user in users:
        score = calculate_score(user)
        ranking_list.append({
            "user_id": user.user_id,
            "score": score
        })

    ranking_list.sort(key=lambda x: x["score"], reverse=True)

    for i, item in enumerate(ranking_list, start=1):
        item["rank"] = i

    return ranking_list