from typing import Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models import Player, Rating
from app.schemas import RatingCreate


def player_exists(db: Session, player_id: int) -> bool:
    return db.query(Player).filter(Player.id == player_id).first() is not None


def add_rating(db: Session, player_id: int, data: RatingCreate) -> dict:
    rating = Rating(player_id=player_id, score=data.score)
    db.add(rating)
    db.commit()
    db.refresh(rating)

    avg = _get_avg(db, player_id)
    return {
        "rating": {"id": rating.id, "player_id": rating.player_id, "score": rating.score},
        "avg_rating": avg,
    }


def get_ratings(db: Session, player_id: int) -> dict:
    ratings = db.query(Rating).filter(Rating.player_id == player_id).all()
    avg = _get_avg(db, player_id)
    return {
        "ratings": [{"id": r.id, "player_id": r.player_id, "score": r.score} for r in ratings],
        "avg_rating": avg,
    }


def _get_avg(db: Session, player_id: int) -> Optional[float]:
    result = (
        db.query(func.avg(Rating.score))
        .filter(Rating.player_id == player_id)
        .scalar()
    )
    return round(result, 2) if result is not None else None
