from typing import Optional
from sqlalchemy import func, asc, desc
from sqlalchemy.orm import Session
from app.models import Player, Rating
from app.schemas import PlayerUpdate


def _player_row_to_dict(player: Player, avg_rating: Optional[float]) -> dict:
    return {
        "id": player.id,
        "name": player.name,
        "country": player.country,
        "club": player.club,
        "image_url": player.image_url,
        "avg_rating": round(avg_rating, 2) if avg_rating is not None else None,
    }


def get_players(
    db: Session,
    q: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
    sort: str = "name",
    order: str = "asc",
) -> list[dict]:
    avg_expr = func.avg(Rating.score).label("avg_rating")

    query = (
        db.query(Player, avg_expr)
        .outerjoin(Rating, Player.id == Rating.player_id)
        .group_by(Player.id)
    )

    if q:
        query = query.filter(Player.name.ilike(f"%{q}%"))

    sort_col = avg_expr if sort == "rating" else Player.name
    query = query.order_by(desc(sort_col) if order == "desc" else asc(sort_col))

    offset = (page - 1) * limit
    rows = query.offset(offset).limit(limit).all()

    return [_player_row_to_dict(player, avg_rating) for player, avg_rating in rows]


def get_player(db: Session, player_id: int) -> Optional[dict]:
    avg_expr = func.avg(Rating.score).label("avg_rating")
    row = (
        db.query(Player, avg_expr)
        .outerjoin(Rating, Player.id == Rating.player_id)
        .group_by(Player.id)
        .filter(Player.id == player_id)
        .first()
    )
    if not row:
        return None
    player, avg_rating = row
    return _player_row_to_dict(player, avg_rating)


def create_player(db: Session, data: dict) -> dict:
    player = Player(**data)
    db.add(player)
    db.commit()
    db.refresh(player)
    return _player_row_to_dict(player, None)


def update_player(db: Session, player_id: int, data: PlayerUpdate) -> Optional[dict]:
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        return None

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(player, field, value)

    db.commit()
    db.refresh(player)
    return get_player(db, player_id)


def delete_player(db: Session, player_id: int) -> bool:
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        return False
    db.delete(player)
    db.commit()
    return True
