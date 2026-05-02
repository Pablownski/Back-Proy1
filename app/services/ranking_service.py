from typing import Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models import Player, Rating, Ranking
from app.schemas import RankingCreate, RankingUpdate

TIER_ORDER = {"S": 0, "A": 1, "B": 2, "C": 3, "D": 4, "F": 5}


def get_ranking(db: Session) -> list[dict]:
    avg_expr = func.avg(Rating.score).label("avg_rating")

    rows = (
        db.query(Ranking, Player, avg_expr)
        .join(Player, Ranking.player_id == Player.id)
        .outerjoin(Rating, Player.id == Rating.player_id)
        .group_by(Ranking.id, Player.id)
        .order_by(Ranking.tier, Ranking.position)
        .all()
    )

    tiers: dict[str, list] = {}
    for ranking, player, avg_rating in rows:
        tiers.setdefault(ranking.tier, []).append(
            {
                "id": player.id,
                "name": player.name,
                "image_url": player.image_url,
                "rating": round(avg_rating, 2) if avg_rating is not None else None,
            }
        )

    sorted_tiers = sorted(tiers.items(), key=lambda x: TIER_ORDER.get(x[0], 99))
    return [{"tier": tier, "players": players} for tier, players in sorted_tiers]


def create_ranking(db: Session, data: RankingCreate) -> Optional[dict]:
    existing = db.query(Ranking).filter(Ranking.player_id == data.player_id).first()
    if existing:
        return None  # player already ranked

    ranking = Ranking(player_id=data.player_id, tier=data.tier, position=data.position)
    db.add(ranking)
    db.commit()
    db.refresh(ranking)
    return {"id": ranking.id, "player_id": ranking.player_id, "tier": ranking.tier, "position": ranking.position}


def update_ranking(db: Session, ranking_id: int, data: RankingUpdate) -> Optional[dict]:
    ranking = db.query(Ranking).filter(Ranking.id == ranking_id).first()
    if not ranking:
        return None

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(ranking, field, value)

    db.commit()
    db.refresh(ranking)
    return {"id": ranking.id, "player_id": ranking.player_id, "tier": ranking.tier, "position": ranking.position}


def delete_ranking(db: Session, ranking_id: int) -> bool:
    ranking = db.query(Ranking).filter(Ranking.id == ranking_id).first()
    if not ranking:
        return False
    db.delete(ranking)
    db.commit()
    return True


def player_exists(db: Session, player_id: int) -> bool:
    return db.query(Player).filter(Player.id == player_id).first() is not None
